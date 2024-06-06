const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

// Directory containing the JSON files
const directoryPath = 'testing-data/';

// Read the directory
fs.readdir(directoryPath, (err, files) => {
  if (err) {
    return console.error('Error reading directory', err);
  }

  files.forEach((file) => {
    if (path.extname(file) === '.json') {
      // Read each JSON file
      const filePath = path.join(directoryPath, file);
      fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
          return console.error(`Error reading file: ${file}`, err);
        }

        // Spawn the Python process for each JSON file
        const pythonProcess = spawn('python3', ['regression.py']);

        // Send the JSON data to the Python process
        pythonProcess.stdin.write(data);
        pythonProcess.stdin.end();

        // Handle the output data from the Python script
        pythonProcess.stdout.on('data', (data) => {
          console.log(`Received from Python for file ${file}: ${data}`);
        });

        // Handle error output from the Python script
        pythonProcess.stderr.on('data', (data) => {
          console.error(`Error from Python for file ${file}: ${data}`);
        });

        // Handle process exit
        pythonProcess.on('close', (code) => {
          console.log(`Python process for file ${file} exited with code ${code}`);
        });
      });
    }
  });
});
