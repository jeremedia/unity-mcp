# Unity Package Development Workflow

## CRITICAL: Let Unity Generate All .meta Files

**DO NOT manually create .meta files!** Unity must generate these automatically to ensure proper GUID assignment and asset tracking.

## Correct Development Workflow

### Initial Setup (After Cloning)

1. **Start Unity Editor First**
   ```bash
   # Open your Unity project
   # Unity 2021.3 or later recommended
   ```

2. **Install Package from Disk**
   - Open Unity Package Manager: `Window > Package Manager`
   - Click the `+` button in top-left
   - Select `Add package from disk...`
   - Navigate to `unity-mcp/UnityMcpBridge/package.json`
   - Click `Open`
   - **Unity will now generate all .meta files automatically**

3. **Verify Installation**
   - Package appears in Package Manager
   - No compilation errors in Console
   - All .meta files generated in package folder

### Development Workflow

1. **Keep Unity Running While Developing**
   - Unity monitors file changes and updates .meta files
   - Compilation happens automatically
   - Asset references stay intact

2. **Adding New Files**
   ```bash
   # CORRECT: Add files while Unity is running
   # Unity immediately generates .meta files

   # WRONG: Add files with Unity closed
   # Missing .meta files cause reference breaks
   ```

3. **Before Committing to Git**
   - Ensure Unity has generated .meta files for all new files
   - Check Console for any errors
   - Verify all .meta files are tracked in git

### Common Mistakes to Avoid

❌ **Never Do This:**
- Manually create .meta files
- Copy .meta files from other assets
- Edit GUIDs in .meta files
- Delete .meta files (unless deleting the asset too)
- Move/rename files outside Unity

✅ **Always Do This:**
- Let Unity generate .meta files
- Perform file operations in Unity Editor
- Commit both files and their .meta files
- Keep .meta files in version control

### Troubleshooting

**Missing .meta files:**
1. Open Unity with the package installed
2. Unity auto-generates missing .meta files
3. Commit the generated .meta files

**Compilation errors after adding files:**
1. Check namespace consistency
2. Verify assembly definition references
3. Ensure all dependencies are installed

**GUID conflicts:**
1. Delete duplicate .meta files
2. Let Unity regenerate with unique GUIDs
3. Fix any broken references

### Release Process

1. Update version in `package.json`
2. Commit all changes including .meta files
3. Tag the release: `git tag v3.4.0-ce.8`
4. Push tags: `git push origin v3.4.0-ce.8`
5. Users update via Package Manager's Update button

## Unity-Specific Package Structure

```
UnityMcpBridge/
├── package.json          # Package manifest
├── package.json.meta     # Unity-generated
├── Editor/              # Editor-only code
│   ├── *.cs            # Editor scripts
│   ├── *.cs.meta       # Unity-generated
│   └── MCPForUnity.Editor.asmdef
├── Runtime/             # Runtime code (if any)
│   ├── *.cs            # Runtime scripts
│   ├── *.cs.meta       # Unity-generated
│   └── MCPForUnity.Runtime.asmdef
└── UnityMcpServer~/     # Hidden folder (Python server)
    └── src/            # Not tracked by Unity
```

## Key Points

1. **Unity owns .meta file generation** - Never create them manually
2. **Work with Unity open** - File monitoring ensures consistency
3. **Version control includes .meta files** - Critical for references
4. **GUIDs are sacred** - Never modify them
5. **Use Unity's Package Manager** - Proper installation workflow

## For This Package Specifically

After removing manually-created .meta files:

1. Open Unity
2. Install package from disk using Package Manager
3. Unity generates correct .meta files for:
   - `Editor/Helpers/BuilderMethodInvoker.cs`
   - `Editor/Helpers/CEBuilderSerializer.cs`
4. Verify no compilation errors
5. Commit Unity-generated .meta files

This ensures proper integration with Unity's asset database and compilation pipeline.