# Smart Medicine Dispenser

A medicine-dispenser backend using FastAPI, PostgreSQL with
TimescaleDB, Neo4j, and a simulated ESP32.

## Components

- FastAPI: backend API
- PostgreSQL + TimescaleDB: sensor readings and event history
- Neo4j: patient, doctor, medicine, and prescription relationships
- Python simulator: generates simulated sensor readings
- ESP32 firmware: planned hardware integration

## Backend setup

1. Open a terminal in the backend directory.
2. Create a virtual environment.
3. Install dependencies:

   pip install -r requirements.txt

4. Copy `.env.example` to `.env`.
5. Configure PostgreSQL and Neo4j credentials.
6. Start the server:

   uvicorn app.main:app --reload

7. Open http://127.0.0.1:8000/docs

## Run the simulator

Open another terminal at the project root.

Install the backend requirements in that terminal's
Python environment if necessary, then run:

python simulator/esp32_simulator.py

## Safety

The simulator generates fake data. It does not authenticate
real patients or operate physical dispensing hardware.

Prescription authorization and hardware interlocks must be
implemented and tested before real medication dispensing.