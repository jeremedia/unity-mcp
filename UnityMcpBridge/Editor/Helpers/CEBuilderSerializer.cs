using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using Newtonsoft.Json.Linq;
using UnityEngine;
using UnityEditor;

// Make it available globally without additional using statements
namespace MCPForUnity.Editor.Helpers
{
    /// <summary>
    /// Extends GameObjectSerializer to extract control surfaces from Curation Engine Builders
    /// by detecting Odin Inspector attributes like [ShowInInspector], [Button], etc.
    /// </summary>
    public static class CEBuilderSerializer
    {
        /// <summary>
        /// Detects if a component is a CE Builder (OK_*_Builder pattern)
        /// </summary>
        public static bool IsCEBuilder(Component component)
        {
            if (component == null || !(component is MonoBehaviour)) return false;

            var typeName = component.GetType().Name;
            return typeName.StartsWith("OK_") && typeName.EndsWith("_Builder");
        }

        /// <summary>
        /// Extracts the control surface (Odin-attributed properties and methods) from a CE Builder.
        /// This defines what can be manipulated via MCP.
        /// </summary>
        public static JObject GetCEBuilderControlSurface(Component builder)
        {
            if (!IsCEBuilder(builder)) return null;

            var surface = new JObject();
            var builderType = builder.GetType();

            // Add builder metadata
            surface["builder_class"] = builderType.Name;
            surface["assembly"] = builderType.Assembly.GetName().Name;

            // Extract properties with Odin attributes
            var properties = new JObject();
            var propertiesWithOdinAttributes = GetPropertiesWithOdinAttributes(builder, builderType);
            foreach (var prop in propertiesWithOdinAttributes)
            {
                properties[prop.Key] = prop.Value;
            }

            // Extract methods with Button/ResponsiveButtonGroup attributes
            var methods = new JObject();
            var methodsWithOdinAttributes = GetMethodsWithOdinAttributes(builderType);
            foreach (var method in methodsWithOdinAttributes)
            {
                methods[method.Key] = method.Value;
            }

            surface["properties"] = properties;
            surface["methods"] = methods;
            surface["property_count"] = properties.Count;
            surface["method_count"] = methods.Count;

            // Try to get the associated Config type if it exists
            var configType = GetAssociatedConfigType(builderType);
            if (configType != null)
            {
                surface["config_type"] = configType.Name;
            }

            return surface;
        }

        /// <summary>
        /// Gets all properties with Odin ShowInInspector attribute
        /// </summary>
        private static Dictionary<string, JObject> GetPropertiesWithOdinAttributes(Component builder, Type builderType)
        {
            var result = new Dictionary<string, JObject>();

            // Get all properties including inherited
            var properties = builderType.GetProperties(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);

            foreach (var prop in properties)
            {
                // Check for ShowInInspector attribute (Odin)
                var showInInspector = prop.GetCustomAttribute(typeof(Attribute))
                    ?.GetType().Name == "ShowInInspectorAttribute";

                if (!showInInspector && prop.GetMethod?.IsPublic != true)
                    continue;

                var propData = new JObject();
                propData["type"] = GetSimplifiedTypeName(prop.PropertyType);
                propData["can_read"] = prop.CanRead;
                propData["can_write"] = prop.CanWrite;

                // Try to get current value safely
                if (prop.CanRead)
                {
                    try
                    {
                        var value = prop.GetValue(builder);
                        propData["current_value"] = value != null ? JToken.FromObject(value) : null;
                    }
                    catch (Exception e)
                    {
                        propData["current_value"] = $"[Error: {e.Message}]";
                    }
                }

                // Detect config path from property getter pattern
                var configPath = DetectConfigPath(prop);
                if (!string.IsNullOrEmpty(configPath))
                {
                    propData["config_path"] = configPath;
                }

                // Get all Odin attributes on this property
                var odinAttrs = GetOdinAttributes(prop);
                if (odinAttrs.Any())
                {
                    propData["odin_attributes"] = JArray.FromObject(odinAttrs);
                }

                result[prop.Name] = propData;
            }

            return result;
        }

        /// <summary>
        /// Gets all methods with Button or ResponsiveButtonGroup attributes
        /// </summary>
        private static Dictionary<string, JObject> GetMethodsWithOdinAttributes(Type builderType)
        {
            var result = new Dictionary<string, JObject>();

            // Get all public methods
            var methods = builderType.GetMethods(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly);

            foreach (var method in methods)
            {
                // Skip property getters/setters and special methods
                if (method.IsSpecialName) continue;

                // Check for Button-related attributes
                var hasButtonAttr = method.GetCustomAttributes()
                    .Any(attr => attr.GetType().Name.Contains("Button") ||
                                attr.GetType().Name.Contains("ResponsiveButtonGroup"));

                // Also include key async methods even without attributes
                var isKeyMethod = method.Name == "Draw" || method.Name == "Erase" || method.Name == "UpdateFromConfig";

                if (!hasButtonAttr && !isKeyMethod)
                    continue;

                var methodData = new JObject();

                // Determine if async (returns Task/UniTask)
                var returnTypeName = method.ReturnType.Name;
                methodData["async"] = returnTypeName.Contains("Task") || returnTypeName.Contains("UniTask");
                methodData["return_type"] = GetSimplifiedTypeName(method.ReturnType);

                // Get parameters
                var parameters = new JArray();
                foreach (var param in method.GetParameters())
                {
                    parameters.Add(new JObject
                    {
                        ["name"] = param.Name,
                        ["type"] = GetSimplifiedTypeName(param.ParameterType),
                        ["has_default"] = param.HasDefaultValue,
                        ["default_value"] = param.HasDefaultValue ?
                            (param.DefaultValue != null ? JToken.FromObject(param.DefaultValue) : null) : null
                    });
                }
                methodData["parameters"] = parameters;

                // Get Odin attributes
                var odinAttrs = GetOdinAttributes(method);
                if (odinAttrs.Any())
                {
                    methodData["odin_attributes"] = JArray.FromObject(odinAttrs);
                }

                result[method.Name] = methodData;
            }

            return result;
        }

        /// <summary>
        /// Attempts to detect the config path from a property's getter implementation
        /// </summary>
        private static string DetectConfigPath(PropertyInfo prop)
        {
            // This is a heuristic - in practice, we'd need to analyze the IL or use conventions
            // Most CE builders follow pattern: get => someConfig.propertyName

            if (!prop.CanRead) return null;

            // For now, use naming convention
            // Typically: roomConfig, wallConfig, pedestalConfig, etc.
            var builderName = prop.DeclaringType?.Name?.Replace("OK_", "").Replace("_Builder", "");
            if (string.IsNullOrEmpty(builderName)) return null;

            var configFieldName = char.ToLower(builderName[0]) + builderName.Substring(1) + "Config";
            return $"{configFieldName}.{prop.Name}";
        }

        /// <summary>
        /// Gets the associated Config type for a Builder (e.g., OK_Room_Builder -> OK_Room_Config)
        /// </summary>
        private static Type GetAssociatedConfigType(Type builderType)
        {
            var configTypeName = builderType.Name.Replace("_Builder", "_Config");

            // Search in the same assembly and CE assemblies
            foreach (var assembly in AppDomain.CurrentDomain.GetAssemblies())
            {
                if (!assembly.FullName.Contains("CurationEngine") &&
                    !assembly.FullName.Contains("CE") &&
                    !assembly.FullName.Contains("OK"))
                    continue;

                var configType = assembly.GetType(configTypeName);
                if (configType != null)
                    return configType;
            }

            return null;
        }

        /// <summary>
        /// Gets all Odin attributes on a member
        /// </summary>
        private static List<string> GetOdinAttributes(MemberInfo member)
        {
            var odinAttrs = new List<string>();

            foreach (var attr in member.GetCustomAttributes())
            {
                var attrName = attr.GetType().Name;

                // Common Odin attributes
                if (attrName.Contains("ShowInInspector") ||
                    attrName.Contains("Button") ||
                    attrName.Contains("BoxGroup") ||
                    attrName.Contains("FoldoutGroup") ||
                    attrName.Contains("TabGroup") ||
                    attrName.Contains("PropertyRange") ||
                    attrName.Contains("MinValue") ||
                    attrName.Contains("MaxValue") ||
                    attrName.Contains("ValueDropdown") ||
                    attrName.Contains("EnumToggleButtons") ||
                    attrName.Contains("ShowIf") ||
                    attrName.Contains("HideIf") ||
                    attrName.Contains("ResponsiveButtonGroup") ||
                    attrName.Contains("PropertySpace") ||
                    attrName.Contains("Indent") ||
                    attrName.Contains("ReadOnly"))
                {
                    odinAttrs.Add(attrName.Replace("Attribute", ""));
                }
            }

            return odinAttrs;
        }

        /// <summary>
        /// Simplifies type names for better readability
        /// </summary>
        private static string GetSimplifiedTypeName(Type type)
        {
            if (type == null) return "unknown";

            // Handle common Unity types
            if (type == typeof(Vector2)) return "Vector2";
            if (type == typeof(Vector3)) return "Vector3";
            if (type == typeof(Vector4)) return "Vector4";
            if (type == typeof(Quaternion)) return "Quaternion";
            if (type == typeof(Color)) return "Color";
            if (type == typeof(Rect)) return "Rect";
            if (type == typeof(Bounds)) return "Bounds";

            // Handle primitives
            if (type == typeof(float)) return "float";
            if (type == typeof(double)) return "double";
            if (type == typeof(int)) return "int";
            if (type == typeof(bool)) return "bool";
            if (type == typeof(string)) return "string";

            // Handle Unity Objects
            if (type.IsSubclassOf(typeof(UnityEngine.Object)))
                return type.Name;

            // Handle collections
            if (type.IsArray)
                return GetSimplifiedTypeName(type.GetElementType()) + "[]";

            if (type.IsGenericType)
            {
                var genericType = type.GetGenericTypeDefinition();
                if (genericType == typeof(List<>))
                    return "List<" + GetSimplifiedTypeName(type.GetGenericArguments()[0]) + ">";
                if (genericType == typeof(Dictionary<,>))
                {
                    var args = type.GetGenericArguments();
                    return $"Dictionary<{GetSimplifiedTypeName(args[0])},{GetSimplifiedTypeName(args[1])}>";
                }
            }

            // Handle Tasks
            if (type.Name.Contains("Task") || type.Name.Contains("UniTask"))
                return "async";

            return type.Name;
        }

        /// <summary>
        /// Generates an MCP tool definition from a Builder's control surface
        /// </summary>
        public static JObject GenerateMCPToolDefinition(JObject controlSurface)
        {
            if (controlSurface == null) return null;

            var builderClass = controlSurface["builder_class"]?.ToString();
            if (string.IsNullOrEmpty(builderClass)) return null;

            // Convert builder name to tool name (e.g., OK_Room_Builder -> place_room)
            var toolName = ConvertBuilderToToolName(builderClass);

            var tool = new JObject();
            tool["name"] = toolName;
            tool["description"] = $"Manipulates {builderClass} in the exhibition space";

            // Build parameters from properties
            var parameters = new JObject();
            var properties = controlSurface["properties"] as JObject;
            if (properties != null)
            {
                foreach (var prop in properties)
                {
                    if (prop.Value["can_write"]?.Value<bool>() == true)
                    {
                        parameters[prop.Key] = new JObject
                        {
                            ["type"] = prop.Value["type"],
                            ["required"] = false,
                            ["description"] = $"Controls {prop.Key}"
                        };
                    }
                }
            }
            tool["parameters"] = parameters;

            // Add available actions from methods
            var actions = new JArray();
            var methods = controlSurface["methods"] as JObject;
            if (methods != null)
            {
                foreach (var method in methods)
                {
                    actions.Add(new JObject
                    {
                        ["action"] = method.Key,
                        ["async"] = method.Value["async"],
                        ["parameters"] = method.Value["parameters"]
                    });
                }
            }
            tool["actions"] = actions;

            return tool;
        }

        /// <summary>
        /// Converts a Builder class name to an MCP tool name
        /// </summary>
        private static string ConvertBuilderToToolName(string builderClass)
        {
            // OK_Room_Builder -> place_room
            // OK_Floor_Pedestal_Builder -> place_floor_pedestal

            var name = builderClass
                .Replace("OK_", "")
                .Replace("_Builder", "")
                .Replace("_", " ");

            // Convert to snake_case
            name = string.Join("_", name.Split(' ').Select(w => w.ToLower()));

            // Prefix with action verb
            if (name.Contains("room") || name.Contains("wall") || name.Contains("pedestal"))
                return "place_" + name;
            if (name.Contains("light"))
                return "configure_" + name;
            if (name.Contains("material"))
                return "apply_" + name;

            return "manage_" + name;
        }
    }
}