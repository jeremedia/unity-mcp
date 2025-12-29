using Newtonsoft.Json.Linq;
using UnityEngine;
using MCPForUnity.Editor.Helpers;
using System;
using System.Collections.Generic;

#if UNITY_EDITOR
using UnityEditor;
#endif

namespace MCPForUnity.Editor.Tools
{
    /// <summary>
    /// MCP tool for getting real-time Unity Editor performance statistics.
    /// Exposes CE_Performance_Monitor data to MCP clients for diagnosing slowdowns.
    /// </summary>
    [McpForUnityTool("get_performance_stats")]
    public static class GetPerformanceStats
    {
        /// <summary>
        /// Handles the get_performance_stats MCP command.
        /// </summary>
        /// <param name="params">
        /// Optional parameters:
        /// - include_markers: array of marker names to filter (optional)
        /// - format: "summary" | "detailed" | "spikes_only" (default: "summary")
        /// </param>
        /// <returns>Performance snapshot with markers, spikes, and recommendations</returns>
        public static object HandleCommand(JObject @params)
        {
            try
            {
                // Check if CE_Performance_Monitor type exists
                var monitorType = Type.GetType("Zinod.Builder.Diagnostics.CE_Performance_Monitor, Assembly-CSharp");

                if (monitorType == null)
                {
                    // Try alternate assembly name
                    monitorType = Type.GetType("Zinod.Builder.Diagnostics.CE_Performance_Monitor, CurationEngineCore");
                }

                if (monitorType == null)
                {
                    return new ErrorResponse(
                        "CE_Performance_Monitor not found. Ensure the Curation Engine Diagnostics system is installed."
                    );
                }

                // Ensure the monitor is running
                var ensureMethod = monitorType.GetMethod("EnsureRunning",
                    System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Static);

                if (ensureMethod != null)
                {
                    ensureMethod.Invoke(null, null);
                }

                // Get the snapshot
                var getSnapshotMethod = monitorType.GetMethod("GetSnapshot",
                    System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Static);

                if (getSnapshotMethod == null)
                {
                    return new ErrorResponse("GetSnapshot method not found on CE_Performance_Monitor");
                }

                var snapshot = getSnapshotMethod.Invoke(null, null);

                if (snapshot == null)
                {
                    return new ErrorResponse("GetSnapshot returned null");
                }

                // Extract format parameter
                string format = @params?["format"]?.ToString()?.ToLower() ?? "summary";

                // Get JSON representation
                var getJsonMethod = monitorType.GetMethod("GetSnapshotJson",
                    System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Static);

                if (getJsonMethod != null)
                {
                    string json = (string)getJsonMethod.Invoke(null, null);

                    // Parse the JSON for manipulation if needed
                    var parsedSnapshot = JObject.Parse(json);

                    // Apply format filtering
                    if (format == "spikes_only")
                    {
                        // Only return spikes array and analysis
                        return new SuccessResponse("Performance spikes retrieved", new
                        {
                            spikes = parsedSnapshot["spikes"],
                            bottleneck = parsedSnapshot["bottleneck"],
                            recommendation = parsedSnapshot["recommendation"]
                        });
                    }
                    else if (format == "summary")
                    {
                        // Return condensed summary
                        var markers = parsedSnapshot["markers"] as JObject;
                        var summaryMarkers = new JObject();

                        if (markers != null)
                        {
                            foreach (var kvp in markers)
                            {
                                var markerData = kvp.Value as JObject;
                                if (markerData != null)
                                {
                                    double elapsedMs = markerData["elapsedMs"]?.Value<double>() ?? 0;
                                    // Only include markers with non-zero elapsed time
                                    if (elapsedMs > 0.001)
                                    {
                                        summaryMarkers[kvp.Key] = new JObject
                                        {
                                            ["elapsedMs"] = elapsedMs,
                                            ["isSpike"] = markerData["isSpike"]
                                        };
                                    }
                                }
                            }
                        }

                        return new SuccessResponse("Performance summary retrieved", new
                        {
                            markers = summaryMarkers,
                            spikes = parsedSnapshot["spikes"],
                            bottleneck = parsedSnapshot["bottleneck"],
                            recommendation = parsedSnapshot["recommendation"]
                        });
                    }
                    else // "detailed"
                    {
                        // Return full snapshot
                        return new SuccessResponse("Performance stats retrieved", parsedSnapshot);
                    }
                }
                else
                {
                    // Fallback: use reflection to extract data directly
                    var snapshotType = snapshot.GetType();

                    var timestampField = snapshotType.GetField("TimestampMs") ??
                                        snapshotType.GetProperty("TimestampMs")?.GetMethod?.Invoke(snapshot, null) as System.Reflection.FieldInfo;
                    var markersField = snapshotType.GetField("Markers");
                    var spikesField = snapshotType.GetField("Spikes");
                    var bottleneckField = snapshotType.GetField("Bottleneck");
                    var recommendationField = snapshotType.GetField("Recommendation");

                    return new SuccessResponse("Performance stats retrieved", new
                    {
                        timestampMs = snapshotType.GetField("TimestampMs")?.GetValue(snapshot),
                        markers = snapshotType.GetField("Markers")?.GetValue(snapshot),
                        spikes = snapshotType.GetField("Spikes")?.GetValue(snapshot),
                        bottleneck = snapshotType.GetField("Bottleneck")?.GetValue(snapshot),
                        recommendation = snapshotType.GetField("Recommendation")?.GetValue(snapshot)
                    });
                }
            }
            catch (Exception e)
            {
                Debug.LogError($"[GetPerformanceStats] Error: {e.Message}\n{e.StackTrace}");
                return new ErrorResponse($"Failed to get performance stats: {e.Message}");
            }
        }
    }
}
