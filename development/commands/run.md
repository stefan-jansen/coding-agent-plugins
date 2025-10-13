---
name: run
description: Execute code or scripts with monitoring and timeout control
allowed-tools: [Bash, Read, Write]
argument-hint: "[script or file to run]"
---

# Run Command

I'll execute your code or scripts with proper monitoring, timeout control, and error handling.

**Input**: $ARGUMENTS

## Usage

```bash
/run script.py              # Execute Python script
/run npm test               # Run npm test command
/run ./build.sh             # Execute shell script
/run "pytest -v tests/"     # Run command with arguments
```

## Phase 1: Command Analysis and Validation

### Input Analysis
Based on the provided arguments: $ARGUMENTS

I'll determine the execution approach:

- **File Execution**: If argument is a file path, execute the file directly
- **Command Execution**: If argument is a command with parameters, execute as shell command
- **Script Detection**: Automatically detect script type and use appropriate interpreter
- **Security Validation**: Ensure command is safe to execute within platform constraints

### Security and Safety
Execution safety is handled through:

1. **Platform Permissions**: Claude Code's built-in permission model controls execution
2. **Tool Restrictions**: Bash tool permissions limit what can be executed
3. **User Validation**: Basic checks for file existence and obvious issues
4. **Timeout Controls**: Automatic timeout to prevent runaway processes

## Phase 2: Execution Environment Setup

### Environment Preparation
Before execution, I'll prepare the environment:

1. **Working Directory**: Ensure we're in the correct project directory
2. **File Validation**: Verify target files exist and are accessible
3. **Permission Check**: Confirm files have appropriate execution permissions
4. **Context Loading**: Load any necessary environment variables or project context

### Execution Method Selection
Choose appropriate execution method based on target:

- **Python Scripts**: Use `python` or `python3` with proper virtual environment
- **Shell Scripts**: Execute with `bash` or `sh` as appropriate
- **Node.js**: Use `node` or `npm` commands for JavaScript execution
- **Make Commands**: Use `make` for Makefile targets
- **Test Runners**: Use appropriate test framework (pytest, jest, etc.)

## Phase 3: Monitored Execution

### Execution with Monitoring
I'll execute the command with comprehensive monitoring:

1. **Start Time Recording**: Log execution start time
2. **Output Capture**: Capture both stdout and stderr
3. **Progress Monitoring**: Show real-time output during execution
4. **Resource Monitoring**: Track execution time and resource usage
5. **Error Detection**: Identify and categorize any errors that occur

### Timeout and Safety Controls
- **Default Timeout**: Reasonable timeout to prevent infinite execution
- **User Interruption**: Ability to interrupt long-running processes
- **Resource Limits**: Prevent excessive resource consumption
- **Safe Termination**: Clean shutdown of processes when needed

### Output Management
- **Real-time Display**: Show output as it's generated
- **Error Highlighting**: Emphasize errors and warnings in output
- **Success Indication**: Clear indication when execution completes successfully
- **Result Summary**: Summarize execution results and timing

## Phase 4: Result Analysis and Reporting

### Execution Results Analysis
After execution completion:

1. **Exit Code Analysis**: Interpret exit codes and their meanings
2. **Output Review**: Analyze stdout and stderr for important information
3. **Error Categorization**: Classify any errors that occurred
4. **Performance Metrics**: Report execution time and resource usage
5. **Success Validation**: Determine if execution met expected outcomes

### Result Display Format
```
🏃 EXECUTION RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Command: [executed command]
Status: ✅ Success | ❌ Failed | ⚠️ Warning
Duration: X.XX seconds
Exit Code: 0

📤 Output:
[stdout content]

❌ Errors (if any):
[stderr content]
```

### Common Execution Patterns

#### Python Script Execution
- Detect virtual environment and activate if needed
- Use appropriate Python version (python3 vs python)
- Handle dependency issues and import errors
- Provide clear error messages for common Python issues

#### Test Execution
- Automatically detect test framework (pytest, jest, etc.)
- Run appropriate test commands
- Parse test results and provide summary
- Highlight failed tests and error locations

#### Build Script Execution
- Execute build scripts with proper environment
- Monitor build progress and output
- Report build success/failure clearly
- Handle common build issues and dependencies

#### Development Server Execution
- Start development servers with monitoring
- Show server startup logs and status
- Handle port conflicts and common issues
- Provide clear startup confirmation

## Phase 5: Error Handling and Troubleshooting

### Error Categories and Resolution
When execution fails, provide specific guidance:

#### File Not Found Errors
- Verify file paths and working directory
- Check for typos in file names
- Suggest correct paths or file locations
- Help with permission issues

#### Permission Errors
- Identify permission problems
- Suggest chmod commands to fix permissions
- Help with ownership issues
- Guide through security considerations

#### Dependency Errors
- Identify missing dependencies or modules
- Suggest installation commands
- Help with version conflicts
- Guide through environment setup

#### Runtime Errors
- Parse error messages for common issues
- Provide specific fix recommendations
- Suggest debugging approaches
- Help with configuration problems

### Recovery Suggestions
For each error type, provide actionable recovery steps:

```
❌ EXECUTION FAILED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Error: [specific error description]
Cause: [likely cause of the error]

🔧 SUGGESTED FIXES:
1. [Specific action to resolve]
2. [Alternative approach]
3. [Additional troubleshooting step]

💡 Next: Try running `[suggested command]`
```

## Phase 6: Integration with Development Workflow

### Test Integration
When running tests:
- Parse test results and provide summary
- Identify failing tests and their locations
- Suggest fixes for common test failures
- Integration with quality assurance workflow

### Build Integration
When running build commands:
- Monitor build progress and dependencies
- Report build artifacts and outputs
- Integration with deployment workflow
- Handle build caching and optimization

### Development Server Integration
When starting development servers:
- Confirm server startup and availability
- Provide access URLs and endpoints
- Monitor for common server issues
- Integration with development workflow

## Success Indicators

- ✅ Command executed successfully without errors
- ✅ Output captured and displayed clearly
- ✅ Execution time and performance metrics recorded
- ✅ Any errors properly categorized and explained
- ✅ Clear success/failure indication provided
- ✅ Helpful troubleshooting guidance when needed

## Examples

### Execute Python Script
```bash
/run script.py
# → Executes Python script with proper environment and monitoring
```

### Run Test Suite
```bash
/run "pytest tests/ -v"
# → Runs pytest with verbose output and result analysis
```

### Execute Build Command
```bash
/run npm run build
# → Executes npm build with progress monitoring
```

### Run Development Server
```bash
/run "python manage.py runserver"
# → Starts Django development server with monitoring
```

---

*Secure script execution with comprehensive monitoring, error handling, and integration with development workflows.*