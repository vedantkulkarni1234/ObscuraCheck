# 🎬 Live Studio - Real-Time Split-Screen Editor

## Overview

The **Live Studio** is a dedicated page that transforms prompt editing into an interactive, real-time experience. It features a unified split-pane interface where you can edit prompts on the left and see live variable preview on the right.

## Key Features

### 1. **Split-Screen Interface**
- **Left Pane (✏️ Editor)**: Syntax-highlighted prompt editor with Ace editor
- **Right Pane (👁️ Live Preview)**: Real-time preview with variable substitution
- Side-by-side editing for optimal workflow

### 2. **Real-Time Variable Detection** 
- ⚡ Variables are automatically detected as you type
- `{{variable_name}}` syntax recognized instantly
- New variables appear in the preview pane immediately
- No need to click "detect variables" - it's on-change!

### 3. **Live Variable Preview**
- Fill in variable values on the right pane
- Preview updates **instantly** with each keystroke
- See the final output in real-time
- Variables highlighted in yellow if missing values

### 4. **Syntax Highlighting**
- Ace editor with Markdown syntax highlighting
- Better readability and fewer typos
- Professional IDE-like experience

### 5. **Quick Actions**
- **💾 Save**: Save or update the prompt
- **📋 Copy Preview**: Copy the substituted preview to clipboard
- **💾 Use & Copy**: Copy preview and stay in editor
- **🏠 Home**: Return to home page
- **🗑️ Delete**: Remove the prompt

## How to Use

### Getting Started

1. Click **🎬 Studio** in the sidebar
2. Select a prompt to edit, or create a new one
3. Edit the prompt content in the left pane
4. See the live preview on the right pane

### Creating a New Prompt

1. From the sidebar, select "Create New" from the prompt selector
2. Enter a title and select a category
3. Add tags (optional)
4. Type your prompt content using `{{variable_name}}` for variables
5. Variables appear automatically in the preview pane
6. Fill in variable values to see the final output
7. Click **💾 Save** to save the prompt

### Editing an Existing Prompt

1. From the sidebar, select a prompt from the dropdown
2. The prompt loads automatically
3. Make your changes in the editor
4. See changes reflected instantly in the preview
5. Click **💾 Save** when done

### Filling in Variables

Each variable type has a different input:
- **Text**: Single-line text input
- **Textarea**: Multi-line text area
- **Select**: Dropdown with predefined options
- **Number**: Numeric input field

Example:
```
Prompt: "Write a {{language}} function for {{task}}"
Variables: 
- language (Text): "Python"
- task (Text): "sorting arrays"

Live Preview: "Write a Python function for sorting arrays"
```

### Using the Copy Feature

**📋 Copy Preview**:
- Copies the final preview text to clipboard
- Ready to paste into your AI tool
- Perfect for quick workflows

**💾 Use & Copy**:
- Copies preview and confirms with success message
- Stay in the editor for more edits
- Streamlined "write and copy" loop

## UI Components

### Left Pane (Editor)
- **Title Input**: Prompt title (required)
- **Category Select**: Choose or create category
- **Tags Input**: Add multiple tags
- **Ace Editor**: Main prompt editor with syntax highlighting

### Right Pane (Preview)
- **Variable Inputs**: Fill in detected variables
- **Live Preview Display**: Shows substituted text
- **Missing Variables Warning**: Alerts for empty variables
- **Copy Buttons**: Quick copy to clipboard actions
- **Statistics**: Character count, word count, variable count

## Advanced Features

### Variable Types

1. **Text** - Simple text input
   - Good for: single words, short phrases
   - Example: `{{username}}`, `{{topic}}`

2. **Textarea** - Multi-line text input
   - Good for: paragraphs, code blocks
   - Example: `{{code_block}}`, `{{description}}`

3. **Select** - Dropdown with predefined options
   - Good for: fixed choices
   - Example: `{{language}}` with options [Python, JavaScript, Go]

4. **Number** - Numeric input
   - Good for: quantities, counts
   - Example: `{{temperature}}`, `{{max_tokens}}`

### Missing Variables

If a variable has no value, it appears as:
- ⚠️ Warning message: "Missing values: {{variable_name}}"
- The variable remains unreplaced in preview: `{{variable_name}}`
- Useful for identifying incomplete fills

### Statistics Display

Located at bottom of preview pane:
- **Characters**: Total character count
- **Words**: Total word count
- **Variables**: Number of detected variables

## Tips & Tricks

### 1. **IDE-Like Feel**
The Live Studio mimics professional code editors:
- Syntax highlighting for readability
- Real-time parsing on each keystroke
- Instant feedback loop
- No need for separate "generate" or "preview" buttons

### 2. **Instant Gratification**
- Type `{{user}}` and immediately see it appear in preview inputs
- Fill in the user value and instantly see the full substitution
- Copy and use immediately
- Highly addictive for power users!

### 3. **Efficient Workflow**
```
Traditional: Edit → Click Generate → Wait → Copy
Live Studio: Edit → See Preview → Copy (instant, real-time)
```

### 4. **Variable Reuse**
- Save a prompt with variables
- Load it later in Studio
- Variable definitions preserved
- Types, defaults, and options remembered

### 5. **Testing Prompts**
- Try different variable values instantly
- See how they affect the output
- Perfect for optimizing prompts before use
- No save required to test

## Keyboard Shortcuts

While editing in the Ace editor:
- **Ctrl/Cmd + S**: Save prompt (if implemented)
- **Ctrl/Cmd + A**: Select all
- **Ctrl/Cmd + Z**: Undo
- **Ctrl/Cmd + Y**: Redo
- **Tab**: Indent
- **Shift + Tab**: Outdent

## Workflow Examples

### Example 1: Quick Prompt Creation
```
1. Type: "Generate a {{language}} {{pattern}} for {{use_case}}"
2. Studio detects 3 variables
3. Fill in:
   - language: "Python"
   - pattern: "Singleton"
   - use_case: "database connection"
4. Preview shows complete prompt
5. Copy and paste into ChatGPT
```

### Example 2: Iterative Refinement
```
1. Load existing prompt
2. Modify text in editor
3. Try different variable values in preview
4. See how each affects the output
5. Save the improved version
```

### Example 3: Variable Type Configuration
```
1. Create prompt with {{model}} variable
2. Save and reload
3. Can change variable type to SELECT
4. Add options: ["gpt-4", "gpt-3.5", "claude-2"]
5. Next time: Use dropdown instead of text input
```

## Performance Notes

- **Real-time Preview**: Updates instantly on every keystroke (no lag)
- **Variable Detection**: Regex pattern matching is very fast (<1ms)
- **Large Prompts**: Optimized for prompts up to 10,000 characters
- **Many Variables**: Can handle 50+ variables efficiently

## Troubleshooting

### Preview Not Updating
- Ensure content has been typed in the editor
- Check that variables use correct syntax: `{{variable_name}}`
- Variable names must start with letter or underscore

### Copy Not Working
- Browser clipboard access may be restricted
- Try using Ctrl/Cmd + C to manually copy from the preview
- Some browsers require HTTPS for clipboard access

### Variable Not Detected
- Check spelling and brackets: `{{var_name}}`
- Variable names must contain only: letters, numbers, underscores
- No spaces inside brackets: `{{ var }}` won't work

### Changes Not Saving
- Ensure validation passes (title, content, category required)
- Check error messages for specific issues
- Use 🏠 Home to return and retry

## Architecture

### Components Used
- **streamlit-ace**: Syntax-highlighted code editor
- **VariableParser**: Extracts and substitutes variables
- **StreamLit Session State**: Maintains editor state across reruns

### Real-Time Processing
1. User types in Ace editor
2. Session state updates (on_change event)
3. VariableParser.extract_variables() runs instantly
4. New variables appear in preview inputs
5. Variable values substituted in preview (VariableParser.substitute_variables())
6. UI reruns to show updated preview

### Data Flow
```
Editor Input (Ace)
    ↓
Session State Update
    ↓
VariableParser.extract_variables()
    ↓
Variable Inputs Generated
    ↓
VariableParser.generate_live_preview()
    ↓
Display Preview
    ↓
User sees instant result
```

## Future Enhancements

Potential features for future versions:
- Syntax highlighting for other formats (JSON, XML, code)
- Undo/redo history
- Multiple prompts comparison
- Variable history/suggestions
- Export to different formats
- Batch variable replacement
- Prompt templates
- Version history/Git-like diffs

## Integration with Other Features

### With Prompt Gallery
- Create complex prompts in Studio
- Save to Gallery for organization
- Browse and load from Gallery

### With 3D Galaxy
- Studio-created prompts appear in Galaxy
- Visual discovery of related prompts
- Links between similar prompts

### With Import/Export
- Import prompts from JSON
- Edit in Studio
- Export with all variables preserved

## Conclusion

The Live Studio transforms prompt editing from a tedious form-fill process into an engaging, interactive experience. With real-time variable detection and instant preview, it feels like working in a professional IDE rather than a web form.

**The instant gratification loop is highly addictive for power users!**

Try it now: **Click 🎬 Studio from the sidebar**
