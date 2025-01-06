
function updateCanvas(analysis) {
    const canvas = document.getElementById('analysisCanvas');
    if (!canvas) {
        console.error('Analysis canvas not found');
        return;
    }
    const ctx = canvas.getContext('2d');

    // Set canvas dimensions
    canvas.width = 800;
    canvas.height = 400;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw angle graphs
    const angles = analysis.knee_angles || {};
    const hipAngles = analysis.hip_angles || {};
    const backAngles = analysis.back_angles || [];

    drawAngleGraph(ctx, canvas, angles.left || [], 'Left Knee Angle', 'red', 0);
    drawAngleGraph(ctx, canvas, angles.right || [], 'Right Knee Angle', 'pink', 50);
    drawAngleGraph(ctx, canvas, hipAngles.left || [], 'Left Hip Angle', 'blue', 150);
    drawAngleGraph(ctx, canvas, hipAngles.right || [], 'Right Hip Angle', 'lightblue', 200);
    drawAngleGraph(ctx, canvas, backAngles, 'Back Angle', 'green', 300);

    // Show canvas
    canvas.classList.remove('d-none');
}

function drawAngleGraph(ctx, canvas, angles, label, color, yOffset) {
    if (!Array.isArray(angles) || angles.length === 0) return;

    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;

    const xScale = canvas.width / angles.length;
    const yScale = 100 / 180; // Convert angles to percentage of 180 degrees

    angles.forEach((angle, i) => {
        const x = i * xScale;
        const y = canvas.height - (angle * yScale) - yOffset;

        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });

    ctx.stroke();

    // Add label
    ctx.fillStyle = color;
    ctx.font = '14px Arial';
    ctx.fillText(label, 10, canvas.height - yOffset - 10);
}
