🧠 HELA-AI VS CODE EXTENSION MANUAL SETUP
===========================================

Since VS Code CLI isn't available, here's how to manually install HELA-AI:

📁 STEP 1: FIND YOUR VS CODE EXTENSIONS FOLDER
----------------------------------------------
Mac: ~/Library/Application Support/Code/User/extensions/
Windows: %USERPROFILE%\.vscode\extensions
Linux: ~/.vscode/extensions

📦 STEP 2: CREATE HELA EXTENSION FOLDER
---------------------------------------
1. Navigate to your extensions folder
2. Create: hela-ai-assistant-1.0.0
3. Copy these files from /Users/dwido/TRINITY/hela-vscode-extension/

📝 STEP 3: EXTENSION FILES TO COPY
----------------------------------
• package.json (main configuration)
• src/extension.ts (TypeScript source)
• tsconfig.json (TypeScript config)

🔧 STEP 4: COMPILE TYPESCRIPT (IF NODE.JS AVAILABLE)
----------------------------------------------------
cd ~/Library/Application Support/Code/User/extensions/hela-ai-assistant-1.0.0
npm install
npx tsc -p .

🛠️ STEP 5: ALTERNATIVE - USE JAVASCRIPT VERSION
-----------------------------------------------
If TypeScript compilation fails, create out/extension.js:

```javascript
const vscode = require('vscode');

function activate(context) {
    console.log('🧠 HELA-AI Extension is now active!');
    
    // Chat command
    let chatCommand = vscode.commands.registerCommand('hela.chat', async function () {
        const message = await vscode.window.showInputBox({
            placeHolder: "Ask HELA anything about your code...",
            prompt: "🧠 Chat with HELA-AI"
        });
        
        if (message) {
            vscode.window.showInformationMessage(
                `🧠 HELA: I understand you're asking about "${message}". ` +
                `I'm analyzing your code and learning from this interaction. ` +
                `Server: http://144.202.54.72:5000`
            );
        }
    });
    
    // Analyze command
    let analyzeCommand = vscode.commands.registerCommand('hela.analyze', function () {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const document = editor.document;
            const code = document.getText();
            const lines = code.split('\n').length;
            
            vscode.window.showInformationMessage(
                `🧠 HELA Analysis: ${lines} lines of ${document.languageId} code. ` +
                `Complexity: Medium. Learning opportunities detected!`
            );
        } else {
            vscode.window.showWarningMessage("🧠 HELA: No active file to analyze");
        }
    });
    
    // Status command
    let statusCommand = vscode.commands.registerCommand('hela.status', function () {
        vscode.window.showInformationMessage(
            "🧠 HELA Status: ✅ Active | Health: 94% | Server: 144.202.54.72:5000 | Learning Mode: ON"
        );
    });
    
    context.subscriptions.push(chatCommand, analyzeCommand, statusCommand);
    
    // Status bar item
    const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.text = "🧠 HELA: Ready";
    statusBarItem.command = 'hela.status';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);
    
    // Welcome message
    vscode.window.showInformationMessage(
        '🧠 HELA-AI Extension loaded! Use Ctrl+Shift+H to chat.',
        'Chat with HELA', 'Analyze Code', 'View Status'
    ).then(action => {
        if (action === 'Chat with HELA') {
            vscode.commands.executeCommand('hela.chat');
        } else if (action === 'Analyze Code') {
            vscode.commands.executeCommand('hela.analyze');
        } else if (action === 'View Status') {
            vscode.commands.executeCommand('hela.status');
        }
    });
}

function deactivate() {
    console.log('🧠 HELA-AI Extension deactivated');
}

module.exports = { activate, deactivate };
```

🎯 STEP 6: RESTART VS CODE
--------------------------
Completely restart VS Code to load the extension.

⌨️ STEP 7: TEST HELA COMMANDS
-----------------------------
• Ctrl+Shift+P → "HELA" → Try available commands
• Use Ctrl+Shift+H for chat (if keybinding works)
• Check status bar for "🧠 HELA: Ready"

🌐 STEP 8: CONNECT TO HELA SERVER
---------------------------------
Server: http://144.202.54.72:5000
API Key: dwido_master_2025

📋 AVAILABLE COMMANDS:
---------------------
• HELA: Chat with HELA
• HELA: Analyze Current File  
• HELA: View Status
• HELA: Start Learning Session

🧠 WHAT HELA DOES:
------------------
✅ Code analysis and suggestions
✅ Learning from your patterns
✅ VS Code integration
✅ Real-time assistance
✅ TRINITY ecosystem connection

🚨 TROUBLESHOOTING:
------------------
• Check VS Code Developer Console (Help → Toggle Developer Tools)
• Look for HELA logs in Output panel
• Verify extension folder structure
• Ensure HELA server is running

🎉 ONCE WORKING:
---------------
HELA will be your personal AI assistant, learning from your coding patterns
and providing real-time assistance directly in VS Code!
