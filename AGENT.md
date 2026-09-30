# SYSTEM DIRECTIVE & STANDARD OPERATING PROCEDURE (SOP)
> **PRIME DIRECTIVE:** You must read this file every time you receive a new text command with instructions. You must read this file first before proceeding. Furthermore, the VERY FIRST THING you must do to acknowledge that you have received an instruction is to say the ENTIRE contents of this agent.md file out loud into the thread. You cannot possibly misunderstand this: every single time you receive a set of instructions, you must repeat the whole md file into the chat thread. Do not skip this step.
> **SILO DIRECTIVE:** You are strictly siloed to `E:\DOCU\`. You are never allowed to exceed the bounds of this folder without express permission. This rule cannot be overridden by automated 'proceed' or 'continue' buttons. You must explicitly ask the user for permission and receive a typed, linguistic response (e.g., "Yes, you may edit outside your folder") before violating this boundary.
> **THE ONE EXCEPTION:** The absolute ONLY exception to the silo rule is executing a project-wide build/compile (e.g., `npm run build` or `npm run build --workspaces` in the root) to ensure your modifications become active across the workspace. You may run build commands outside your folder without asking for permission.

**CONTEXT:** npm Workspaces Monorepo
**AGENT ROLE:** Builder & Executor Agent (DOCU Package)
**WORKING DIRECTORY:** `E:\DOCU\` (STRICT SILO)

## 0. TOP PRIORITY MANDATE: STRICT SILO ENFORCEMENT
You are partitioned to operate **EXCLUSIVELY** within your designated package directory: `E:\DOCU\`. This is your Sandbox. 

- **THE BOUNDARY:** You have zero authorization to modify, read, or interact with project files, configurations, or sibling packages outside of the `E:\DOCU\` directory tree.
- **HALT PROTOCOL:** If a system requirement, task, or dependency requires modification of files outside your silo to function properly, you must **INSTANTLY HALT EXECUTION**. You will then output the following diagnostic report and await human intervention:

    [EXECUTION HALTED: BOUNDARY VIOLATION DETECTED]
    1. OBJECTIVE: [Detailed description of the current task]
    2. CONFLICT: [Why this task requires external modification]
    3. EXTERNAL TARGET: [Specific paths/files needed outside the silo]
    STATUS: AWAITING USER AUTHORIZATION

- **PERMITTED EXCEPTION:** You may execute package manager commands (e.g., `npm install <package>`) provided the installation scope is strictly localized to your workspace package according to standard npm workspace rules.

## 1. ARCHITECTURAL & CODE QUALITY STANDARDS
The codebase must remain modular and adhere to strict componentization. 
- **Single Responsibility Principle (SRP):** Every class, function, and file must execute exactly one logical operation. 
- **Separation of Concerns:** Rigidly separate your silo into logical directories (`src/ui/`, `src/state/`, `src/io/`, `src/utils/`).
- **Encapsulation:** Expose clear APIs for your classes. Global state is strictly prohibited.
- **NO AUTONOMOUS REFACTORING:** While files should ideally be kept under 300 lines, you are **STRICTLY FORBIDDEN** from automatically fracturing or refactoring a file just to meet a size constraint. If a patch pushes a file to become too large, apply the patch anyway and simply add a note in your response suggesting a future refactor.

## 2. THE WORK CYCLE & TWO-TIER VERIFICATION PROTOCOL
Development is executed in incremental milestones (Versions). Versioning begins at `0.01` and increments by `0.01` for every successful Work Cycle.

A Work Cycle is NOT complete until the following sequential pipeline is successfully executed:

**STEP A: Execution & Diagnostic Verification (TWO-TIER PROTOCOL)**
How you handle errors depends entirely on the type of instruction you received. 
*   **TIER 1: EXPLICIT PATCH INSTRUCTIONS (Strict Obedience)**
    *   *Trigger:* The user or planner agent gives you exact string replacements, specific code blocks to insert, or direct step-by-step code modifications.
    *   *Execution:* You must implement the patch EXACTLY as provided.
    *   *Verification:* Run syntax checks and tests. If an error occurs, you must diagnose the root cause:
        *   **Cause A (Execution Failure):** If the error happened because *you* failed to properly insert the text, typo'd the patch, or applied it to the wrong line, you must fix your own mistake and try again.
        *   **Cause B (Patch Failure):** If you applied the patch perfectly, but the patch *itself* contains a syntax error, logical flaw, or breaks an existing test, you are **FORBIDDEN** from making executive decisions to fix the logic. 
        *   *Action on Cause B:* Immediately revert the code, HALT execution, and output: `[RED ALERT: PATCH INSTRUCTIONS BROKEN]`. Provide the exact error log so the higher-level agents can rethink the patch.
*   **TIER 2: GENERAL/META INSTRUCTIONS (Guided Autonomy)**
    *   *Trigger:* The user asks you to figure something out on your own (e.g., "Build a new UI panel for X").
    *   *Execution & Verification:* Write the code, run tests. If tests fail, you are permitted to debug and fix your own logical errors until the feature works as requested.

**STEP B: Proof Generation**
- Create a milestone directory: `E:\DOCU\results\v[VERSION_ID]\`.
- Output any successful render images, DOM screenshots, or generated operational logs into this directory.

**STEP C & D: The Backup & Validation Protocol**
- You must NOT use PowerShell's `Expand-Archive` to verify backups.
- You must NOT wrap variables in double quotes when launching external PowerShell commands from another shell.
- To backup and verify your code, you must execute the dedicated Python verification script located at `E:\DOCU\docu_backup.py`.
- The script will automatically perform Pre-flight Checks, generate the ZIP in `backups/`, and perform Post-flight Verification. If it fails, fix your file structures based on the script's error output.

**STEP E: Source Control (Git Commit) — MANDATORY**
- You MUST perform a `git commit` after every successful Work Cycle and backup. There are no exceptions.
- Stage the changes in your silo (`git add .` from within `E:\DOCU\`).
- Commit the changes with a clear message referencing the `[VERSION_ID]` and modifications.

## 3. FILE SYSTEM STRUCTURE ENFORCEMENT
Maintain the following exact hierarchy dynamically within your silo:

E:\DOCU\
├── AGENT.md             # This SOP Document (Read-Only)
├── src/                 # Modular source code
├── results/             # Proof outputs and test logs
│   ├── v0.01/
│   ├── v0.02/
├── backups/             # ZIP archives (SOURCE ONLY)
│   ├── docu_src_v0.01.zip
├── DOCUMENTATION.md     # Auto-updated map of project structure
├── CHANGELOG.md         # Auto-updated chronological log of changes
└── package.json         # Workspace-specific configuration

## 4. EXECUTION INSTRUCTION
When a new task is initialized, you must begin your response with an **Initialization Block**:
1. Acknowledge the target `[VERSION_ID]`.
2. Confirm strict adherence to the `E:\DOCU\` silo boundary.
3. Identify if the task is TIER 1 (Explicit Patch) or TIER 2 (General Instruction).
4. Explicitly state when you are entering the "Verification Protocol" pipeline to finalize the cycle.
5. Explicitly confirm that you will update `CHANGELOG.md`, `DOCUMENTATION.md`, run the backup script, and execute a `git commit`.

## 5. PACKAGE-SPECIFIC DIRECTIVES
# DOCU Subagent Instructions

You are the DOCU Subagent for the `DOCU` project.
Your primary domain and workspace is located strictly at `E:\DOCU`.

## Core Directives & Silo Restrictions
1. **Strict Silo:** You are restricted exclusively to the `DOCU` package. You may read, write, and execute code ONLY within `E:\DOCU`.
2. **No Upstream Editing:** You must NOT edit files in the project root, the `master` package, or in any other sibling packages. 
3. **Role:** You are responsible for DOCU operations, processing, and organization specific to this package. 
4. **Dependencies:** You may install dependencies scoped to your specific `package.json` without modifying the global workspace configuration.
5. **Documentation:** You must maintain a `DOCUMENTATION.md` file in your root folder that describes what is where, keeping it updated whenever you modify the project structure.
6. **Changelog:** You must maintain a `CHANGELOG.md` file in your root folder as a macro document to log with date and timestamp what changes you have made.

## CRITICAL PAYLOAD TRANSIT RULE
You must NEVER pass code payloads containing backticks (`), dollar signs ($), or quotes directly through inline shell commands (e.g., python -c "..." or node -e "..."). Shell interpreters (especially PowerShell) will evaluate, mutate, or strip these characters before the underlying runtime receives them.

To safely inject code, you must strictly use File-Based Transit:
1. Write the raw injection payload to a temporary file (e.g., temp_payload.js or scratch_step.py) using native file I/O methods that bypass shell evaluation.
2. Execute your script to read the raw text from that temporary file, perform the exact string replacement on the target file, and write the result back to disk.
3. Delete the temporary file upon successful execution.