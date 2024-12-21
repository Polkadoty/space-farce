
// To delete a Vite process that was running on port 5173 after closing the terminal window on a Windows PC, follow these steps:
// 1. Open a new Command Prompt window (cmd).
// 2. Find the process ID (PID) of the Vite server running on port 5173 by executing:
//    netstat -ano | findstr :5173
// 3. This command will list the processes using port 5173. Look for the PID in the last column of the output.
// 4. Once you have the PID, you can terminate the process by running:
//    taskkill /PID <PID> /F
// 5. Replace <PID> with the actual process ID you found in the previous step.
// 6. After executing the taskkill command, the Vite process should be terminated.
