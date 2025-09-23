using UnityEngine;
using UnityEditor;
using System;
using System.Reflection;
using System.Collections.Generic;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace UnityMcp.Editor.Helpers
{
    /// <summary>
    /// Helper class for invoking methods on Unity Builder components via MCP.
    /// Supports Odin-exposed methods like AddPedestal, RemoveBuilder, etc.
    /// </summary>
    public static class BuilderMethodInvoker
    {
        /// <summary>
        /// Invokes a method on a Builder component
        /// </summary>
        public static object InvokeBuilderMethod(
            GameObject target,
            string componentTypeName,
            string methodName,
            Dictionary<string, object> parameters = null)
        {
            if (target == null)
            {
                throw new ArgumentNullException(nameof(target), "Target GameObject is null");
            }

            // Get the component by type name (support both simple name and full type name)
            Component component = null;
            foreach (var comp in target.GetComponents<Component>())
            {
                if (comp != null &&
                    (comp.GetType().Name == componentTypeName ||
                     comp.GetType().FullName == componentTypeName ||
                     comp.GetType().ToString() == componentTypeName))
                {
                    component = comp;
                    break;
                }
            }

            if (component == null)
            {
                throw new InvalidOperationException($"Component '{componentTypeName}' not found on GameObject '{target.name}'");
            }

            // Get the method
            Type componentType = component.GetType();
            MethodInfo method = null;

            // Handle method overloads
            if (parameters != null && parameters.Count > 0)
            {
                // Try to find method with parameters
                method = FindMethodWithParameters(componentType, methodName, parameters);
            }
            else
            {
                // Get parameterless method
                method = componentType.GetMethod(methodName, BindingFlags.Public | BindingFlags.Instance, null, Type.EmptyTypes, null);
            }

            if (method == null)
            {
                throw new InvalidOperationException($"Method '{methodName}' not found on component '{componentTypeName}'");
            }

            // Prepare parameters for invocation
            object[] invokeParams = null;
            if (parameters != null && parameters.Count > 0)
            {
                invokeParams = PrepareParameters(method, parameters);
            }

            // Check if method is async
            bool isAsync = method.ReturnType == typeof(Task) ||
                          (method.ReturnType.IsGenericType && method.ReturnType.GetGenericTypeDefinition() == typeof(Task<>));

            // Invoke the method
            object result = null;
            try
            {
                if (isAsync)
                {
                    // Handle async method
                    var task = method.Invoke(component, invokeParams) as Task;
                    if (task != null)
                    {
                        // For Unity, we can't really await properly in editor code
                        // So we'll start the task and return immediately
                        task.ContinueWith(t =>
                        {
                            if (t.IsFaulted)
                            {
                                Debug.LogError($"Async method {methodName} failed: {t.Exception}");
                            }
                            else
                            {
                                Debug.Log($"Async method {methodName} completed successfully");
                            }
                        });

                        result = new { status = "async_started", message = $"Async method {methodName} has been started" };
                    }
                }
                else
                {
                    // Synchronous method
                    result = method.Invoke(component, invokeParams);
                }

                // Mark the scene as dirty if we modified something
                EditorUtility.SetDirty(target);
                UnityEditor.SceneManagement.EditorSceneManager.MarkSceneDirty(target.scene);

                return new
                {
                    success = true,
                    methodName = methodName,
                    componentType = componentTypeName,
                    targetName = target.name,
                    result = result
                };
            }
            catch (Exception ex)
            {
                Debug.LogError($"Failed to invoke method {methodName}: {ex.Message}");
                throw new InvalidOperationException($"Failed to invoke method: {ex.Message}", ex);
            }
        }

        /// <summary>
        /// Find method that matches the provided parameters
        /// </summary>
        private static MethodInfo FindMethodWithParameters(Type componentType, string methodName, Dictionary<string, object> parameters)
        {
            var methods = componentType.GetMethods(BindingFlags.Public | BindingFlags.Instance);

            foreach (var method in methods)
            {
                if (method.Name != methodName) continue;

                var methodParams = method.GetParameters();

                // Special handling for common parameter patterns
                if (parameters.ContainsKey("position") && methodParams.Length == 1 && methodParams[0].ParameterType == typeof(Vector3))
                {
                    return method; // Found AddPedestal(Vector3) overload
                }
                else if (parameters.ContainsKey("rect") && methodParams.Length == 1 && methodParams[0].ParameterType == typeof(Rect))
                {
                    return method; // Found AddPedestal(Rect) overload
                }
                else if (parameters.ContainsKey("preset") && methodParams.Length == 1)
                {
                    // Check if parameter is a preset type
                    if (methodParams[0].ParameterType.Name.Contains("Preset"))
                    {
                        return method;
                    }
                }
            }

            // If no specific match, return the first method with matching name
            return componentType.GetMethod(methodName, BindingFlags.Public | BindingFlags.Instance);
        }

        /// <summary>
        /// Prepare parameters for method invocation
        /// </summary>
        private static object[] PrepareParameters(MethodInfo method, Dictionary<string, object> parameters)
        {
            var methodParams = method.GetParameters();
            var invokeParams = new object[methodParams.Length];

            for (int i = 0; i < methodParams.Length; i++)
            {
                var paramInfo = methodParams[i];
                object value = null;

                // Try to find parameter by name
                if (parameters.ContainsKey(paramInfo.Name))
                {
                    value = parameters[paramInfo.Name];
                }
                // Special handling for position parameter
                else if (parameters.ContainsKey("position") && paramInfo.ParameterType == typeof(Vector3))
                {
                    value = parameters["position"];
                }
                // Special handling for rect parameter
                else if (parameters.ContainsKey("rect") && paramInfo.ParameterType == typeof(Rect))
                {
                    value = parameters["rect"];
                }

                // Convert value to correct type
                if (value != null)
                {
                    invokeParams[i] = ConvertParameter(value, paramInfo.ParameterType);
                }
                else if (paramInfo.HasDefaultValue)
                {
                    invokeParams[i] = paramInfo.DefaultValue;
                }
                else
                {
                    invokeParams[i] = null;
                }
            }

            return invokeParams;
        }

        /// <summary>
        /// Convert parameter value to the expected type
        /// </summary>
        private static object ConvertParameter(object value, Type targetType)
        {
            // Handle Vector3
            if (targetType == typeof(Vector3))
            {
                if (value is JArray jArray)
                {
                    var values = jArray.ToObject<float[]>();
                    if (values.Length >= 3)
                    {
                        return new Vector3(values[0], values[1], values[2]);
                    }
                }
                else if (value is float[] floatArray && floatArray.Length >= 3)
                {
                    return new Vector3(floatArray[0], floatArray[1], floatArray[2]);
                }
                else if (value is List<float> floatList && floatList.Count >= 3)
                {
                    return new Vector3(floatList[0], floatList[1], floatList[2]);
                }
            }
            // Handle Rect
            else if (targetType == typeof(Rect))
            {
                if (value is JObject jObj)
                {
                    return new Rect(
                        jObj["x"]?.Value<float>() ?? 0,
                        jObj["y"]?.Value<float>() ?? 0,
                        jObj["width"]?.Value<float>() ?? 1,
                        jObj["height"]?.Value<float>() ?? 1
                    );
                }
                else if (value is Dictionary<string, object> dict)
                {
                    return new Rect(
                        Convert.ToSingle(dict.GetValueOrDefault("x", 0f)),
                        Convert.ToSingle(dict.GetValueOrDefault("y", 0f)),
                        Convert.ToSingle(dict.GetValueOrDefault("width", 1f)),
                        Convert.ToSingle(dict.GetValueOrDefault("height", 1f))
                    );
                }
            }
            // Handle primitives
            else if (targetType == typeof(float))
            {
                return Convert.ToSingle(value);
            }
            else if (targetType == typeof(int))
            {
                return Convert.ToInt32(value);
            }
            else if (targetType == typeof(bool))
            {
                return Convert.ToBoolean(value);
            }
            else if (targetType == typeof(string))
            {
                return value.ToString();
            }

            // Try direct conversion
            try
            {
                return Convert.ChangeType(value, targetType);
            }
            catch
            {
                // If conversion fails, return the value as-is and hope for the best
                return value;
            }
        }

        /// <summary>
        /// Get available methods for a component type
        /// </summary>
        public static List<string> GetAvailableMethods(string componentTypeName)
        {
            var methods = new List<string>();

            // Try to find the type
            Type componentType = null;
            foreach (var assembly in AppDomain.CurrentDomain.GetAssemblies())
            {
                componentType = assembly.GetType(componentTypeName);
                if (componentType != null) break;

                // Try with common namespaces
                componentType = assembly.GetType($"Zinod.Builder.{componentTypeName}");
                if (componentType != null) break;
            }

            if (componentType == null)
            {
                return methods;
            }

            // Get all public instance methods
            var methodInfos = componentType.GetMethods(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly);

            foreach (var method in methodInfos)
            {
                // Skip property getters/setters and special methods
                if (method.IsSpecialName) continue;
                if (method.Name.StartsWith("get_") || method.Name.StartsWith("set_")) continue;

                // Look for methods with Odin attributes (simplified check)
                var attributes = method.GetCustomAttributes(false);
                foreach (var attr in attributes)
                {
                    var attrTypeName = attr.GetType().Name;
                    if (attrTypeName.Contains("Button") || attrTypeName.Contains("ResponsiveButton"))
                    {
                        methods.Add(method.Name);
                        break;
                    }
                }
            }

            return methods;
        }
    }
}