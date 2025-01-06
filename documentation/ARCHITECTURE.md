# Technical Architecture

## System Components

```
+------------------------+     +------------------------+
|    Client Browser      |     |    Flask Server       |
|                       |     |                       |
|  +----------------+   |     |  +----------------+   |
|  |  Video Input   |   |     |  |   WebSocket   |   |
|  +----------------+   |     |  |    Server     |   |
|         |            |     |  +----------------+   |
|         v            |     |         |            |
|  +----------------+   |     |         v            |
|  |   WebSocket    |<--+-----+->+----------------+  |
|  |    Client      |   |     |  |  MediaPipe    |  |
|  +----------------+   |     |  |    Pose       |  |
|         |            |     |  +----------------+  |
|         v            |     |         |           |
|  +----------------+   |     |         v           |
|  |    Canvas      |   |     |  +----------------+ |
|  | Visualization  |   |     |  | Pose Analyzer  | |
|  +----------------+   |     |  +----------------+ |
|         |            |     |         |           |
|         v            |     |         v           |
|  +----------------+   |     |  +----------------+ |
|  |   Feedback     |   |     |  |    Form       | |
|  |    Display     |<--+-----+--|  Classifier   | |
|  +----------------+   |     |  +----------------+ |
|                       |     |                     |
+------------------------+     +---------------------+

```

## Data Flow

1. Video Input
   ```
   User Input -> Video Stream -> WebSocket -> Server
   ```

2. Analysis Pipeline
   ```
   Video Frame -> MediaPipe -> Pose Detection -> Analysis -> Classification
   ```

3. Feedback Loop
   ```
   Classification -> Feedback Generation -> WebSocket -> Client Display
   ```

## Component Interactions

### Client Side
- Video capture and streaming
- Real-time visualization
- Feedback display
- User interface management

### Server Side
- WebSocket communication
- Pose detection
- Analysis computation
- Form classification

### Data Processing
- Frame extraction
- Landmark detection
- Metric calculation
- Form analysis

## Technology Stack

```
Frontend:
- HTML5 / CSS3
- JavaScript
- Socket.IO Client
- Bootstrap Dark Theme

Backend:
- Flask
- Flask-SocketIO
- MediaPipe
- OpenCV
- NumPy

Communication:
- WebSocket (Socket.IO)
- HTTP/HTTPS
```
