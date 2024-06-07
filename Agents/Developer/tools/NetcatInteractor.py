import subprocess
import socket
from agency_swarm.tools import BaseTool
from pydantic import Field

# Subprocess registry to track running servers by ID
subprocess_registry = {}

class NetcatServer(BaseTool):
    port: int = Field(..., gt=0, lt=65536, description="The port on which the Netcat server will listen.")

    def run(self):
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        process = subprocess.Popen(['nc', '-l', local_ip, self.port], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


        # Generate a unique identifier for the subprocess
        process_id = str(id(process))
        subprocess_registry[process_id] = process

        return (f"Netcat server is running on subprocess with process_id: {process_id} and it listening on ip:port {local_ip}:{self.port}.", 
                f"info: Netcat server started. Use process ID f{process_id} to interact.")

class NetcatInteractor(BaseTool):
    process_id: str = Field(..., description="The ID of the running Netcat server subprocess.")

    def send_command(self, command: str):
        process = subprocess_registry.get(self.process_id)
        
        if process and process.poll() is None:
            process.stdin.write(command + "\n")
            process.stdin.flush()
            return process.stdout.readline().strip()
        else:
            return "Netcat server is not running or the ID is invalid."

# if __name__ == "__main__":
#     nc_tool = NetcatServer(port=9999)
#     server_info = nc_tool.run()
#     interactor = NetcatInteractor(process_id=server_info["process_id"])
#     print(interactor.send_command("whoami"))

