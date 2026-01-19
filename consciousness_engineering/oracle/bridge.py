import socket
import json
import struct
import time
import os
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class PhysicsTelemetry:
    t: float
    entropy: float
    coherence: float
    order_parameter: float
    resonance_score: float
    dominant_primes: List[int]
    twist_closed: bool

class TinyAlephOracle:
    """
    The Hyperdimensional Gyrometer.
    
    Acts as a bridge to the TinyAleph Node.js Physics Engine.
    Uses standard TCP sockets for zero-dependency communication.
    """
    def __init__(self, port: int = 5555, server_path: str = None):
        self.port = port
        self.host = 'localhost'
        self._connect()
        
    def _connect(self):
        try:
            print(f"🔮 Connecting to TinyAleph Oracle on {self.host}:{self.port}...")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            print("✅ Connected.")
        except ConnectionRefusedError:
            print("❌ Connection refused. Is the server running?")
            self.sock = None

    def _send_json(self, data: Dict[str, Any]):
        if not self.sock:
            self._connect()
            if not self.sock: return
            
        msg = json.dumps(data).encode('utf-8')
        # Prefix with 4-byte length
        header = struct.pack('>I', len(msg))
        self.sock.sendall(header + msg)

    def _recv_json(self) -> Dict[str, Any]:
        if not self.sock: return {}
        
        # Read 4-byte length
        header = self._recv_all(4)
        if not header: return {}
        
        msg_len = struct.unpack('>I', header)[0]
        data = self._recv_all(msg_len)
        return json.loads(data)

    def _recv_all(self, n: int) -> bytes:
        data = b''
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet: return None
            data += packet
        return data

    def ping(self) -> bool:
        """Check if the Oracle is online."""
        try:
            self._send_json({"cmd": "ping"})
            msg = self._recv_json()
            return msg.get("status") == "pong"
        except Exception as e:
            print(f"Oracle offline: {e}")
            return False

    def measure_resonance(self, text: str) -> Dict[str, Any]:
        """
        Send text to the Oracle to measure its Prime Resonance and Twist Closure.
        """
        self._send_json({
            "cmd": "measure_resonance",
            "text": text
        })
        return self._recv_json()

    def update_physics(self, primes: List[int]) -> PhysicsTelemetry:
        """
        Feed Prime activations into the Sedenion Oscillator Bank.
        """
        self._send_json({
            "cmd": "update_physics",
            "primes": primes
        })
        data = self._recv_json()
        return PhysicsTelemetry(**data)

    def get_trajectory(self) -> List[Any]:
        """Get the recent Sedenion trajectory points."""
        self._send_json({"cmd": "get_trajectory"})
        return self._recv_json()
