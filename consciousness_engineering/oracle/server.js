
const net = require('net');
const path = require('path');

// Import TinyAleph from the local external directory
// Adjust path as needed based on where this script is located
const TINYALEPH_ROOT = path.resolve(__dirname, '../../../Ada-Consciousness-Research/external/tinyaleph');

// Specific Imports for robustness
const { EnochianEngine, SedenionElement } = require(path.join(TINYALEPH_ROOT, 'core/enochian-vocabulary.js'));
const { PrimeonZLadderMulti } = require(path.join(TINYALEPH_ROOT, 'physics/primeon_z_ladder_multi.js'));


// Initialize Engines
const enochian = new EnochianEngine();
const physics = new PrimeonZLadderMulti({
    N: 128,          // 128 rungs (Primes)
    d: 1,            // 1 internal dimension
    J: 0.1,          // Coupling strength
    zChannels: [
        { name: 'fast', dz: 1, leak: 0.1, decay: 0.05 },
        { name: 'slow', dz: 1, leak: 0.01, decay: 0.001 },
        { name: 'eternal', dz: 1, leak: 0.001, decay: 0.0 }
    ]
});

console.log("✅ Engines Initialized.");

// TCP Server
const PORT = 5555;
const server = net.createServer((socket) => {
    console.log('🔗 Client connected');

    socket.on('data', (data) => {
        // Handle Length-Prefixed JSON
        // Note: In a production server we would buffer data until we have a full message.
        // For this prototype, we assume the Python client sends clean packets or simple buffering.
        // We actally need a small buffer handler here for robustness.

        handleDataChunk(socket, data);
    });

    socket.on('end', () => {
        console.log('🔌 Client disconnected');
    });
});

let buffer = Buffer.alloc(0);

function handleDataChunk(socket, chunk) {
    buffer = Buffer.concat([buffer, chunk]);

    while (buffer.length >= 4) {
        const len = buffer.readUInt32BE(0);
        if (buffer.length < 4 + len) {
            return; // Wait for more data
        }

        const msgBuffer = buffer.slice(4, 4 + len);
        buffer = buffer.slice(4 + len);

        try {
            const msg = JSON.parse(msgBuffer.toString());
            const response = processCommand(msg);
            sendResponse(socket, response);
        } catch (e) {
            console.error("Error processing message:", e);
            sendResponse(socket, { error: e.message });
        }
    }
}

function sendResponse(socket, data) {
    const jsonStr = JSON.stringify(data);
    const msg = Buffer.from(jsonStr);
    const header = Buffer.alloc(4);
    header.writeUInt32BE(msg.length, 0);
    socket.write(Buffer.concat([header, msg]));
}

function processCommand(cmd) {
    switch (cmd.cmd) {
        case 'ping':
            return { status: 'pong', t: Date.now() };

        case 'measure_resonance':
            // Analyze text using Enochian Engine
            const text = cmd.text || "";
            const primes = enochian.primeSignature(text);
            const twist = enochian.hasTwistClosure(text);
            const sedenion = enochian.toSedenion(text);

            return {
                text: text,
                primes: primes.slice(0, 10), // Limit output
                twist_closed: twist.valid,
                twist_angle: twist.totalAngle,
                sedenion_norm: sedenion.norm(),
                resonance_score: twist.closeness < 10 ? (1 - twist.closeness / 360) : 0
            };

        case 'update_physics':
            // Excite the physics engine with primes
            const inputPrimes = cmd.primes || [];
            if (inputPrimes.length > 0) {
                physics.excitePrimes(inputPrimes, 1.0);
            }

            // Evolve time
            const metrics = physics.step(0.1);

            return {
                t: metrics.t,
                entropy: metrics.core.entropy,
                coherence: metrics.core.coherence,
                order_parameter: metrics.core.orderParameter,
                resonance_score: metrics.totalZEntropy, // Inverse entropy proxy
                twist_closed: false,
                dominant_primes: inputPrimes
            };

        case 'get_trajectory':
            return {
                status: "not_implemented_yet"
            };

        default:
            return { error: 'Unknown command' };
    }
}

server.listen(PORT, () => {
    console.log(`🚀 TinyAleph Oracle Server listening on port ${PORT}`);
});
