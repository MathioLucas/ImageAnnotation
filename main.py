import React, { useState, useRef, useEffect } from 'react';

const ImageAnnotator = () => {
  const [annotations, setAnnotations] = useState([]);
  const [isDrawing, setIsDrawing] = useState(false);
  const [currentBox, setCurrentBox] = useState(null);
  const [selectedBox, setSelectedBox] = useState(null);
  const [label, setLabel] = useState('');
  const canvasRef = useRef(null);
  const containerRef = useRef(null);

  const [image, setImage] = useState(null);
  const imageRef = useRef(null);

  useEffect(() => {
    // Create demo image
    const img = new Image();
    img.src = '/api/placeholder/800/600';
    img.onload = () => {
      setImage(img);
      drawCanvas();
    };
  }, []);

  const drawCanvas = () => {
    if (!canvasRef.current || !image) return;
    const ctx = canvasRef.current.getContext('2d');
    ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    ctx.drawImage(image, 0, 0, canvasRef.current.width, canvasRef.current.height);

    // Draw all annotations
    annotations.forEach((box, index) => {
      ctx.strokeStyle = selectedBox === index ? '#00ff00' : '#ff0000';
      ctx.lineWidth = 2;
      ctx.strokeRect(box.x, box.y, box.width, box.height);

      if (box.label) {
        ctx.font = '14px Arial';
        ctx.fillStyle = 'white';
        ctx.fillRect(box.x, box.y - 20, ctx.measureText(box.label).width + 10, 20);
        ctx.fillStyle = 'black';
        ctx.fillText(box.label, box.x + 5, box.y - 5);
      }
    });

    // Draw current box if drawing
    if (currentBox) {
      ctx.strokeStyle = '#ff0000';
      ctx.lineWidth = 2;
      ctx.strokeRect(currentBox.x, currentBox.y, currentBox.width, currentBox.height);
    }
  };

  useEffect(() => {
    drawCanvas();
  }, [annotations, currentBox, selectedBox]);

  const handleMouseDown = (e) => {
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Check if clicked inside existing box
    const clickedBoxIndex = annotations.findIndex(box => 
      x >= box.x && x <= box.x + box.width &&
      y >= box.y && y <= box.y + box.height
    );

    if (clickedBoxIndex >= 0) {
      setSelectedBox(clickedBoxIndex);
    } else {
      setIsDrawing(true);
      setCurrentBox({ x, y, width: 0, height: 0 });
      setSelectedBox(null);
    }
  };

  const handleMouseMove = (e) => {
    if (!isDrawing || !currentBox) return;

    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    setCurrentBox(prev => ({
      ...prev,
      width: x - prev.x,
      height: y - prev.y
    }));
  };

  const handleMouseUp = () => {
    if (isDrawing && currentBox) {
      const newBox = {
        ...currentBox,
        label: ''
      };
      setAnnotations(prev => [...prev, newBox]);
      setSelectedBox(annotations.length);
    }
    setIsDrawing(false);
    setCurrentBox(null);
  };

  const handleLabelChange = (e) => {
    setLabel(e.target.value);
  };

  const handleLabelSubmit = (e) => {
    e.preventDefault();
    if (selectedBox !== null && label.trim()) {
      setAnnotations(prev => prev.map((box, i) => 
        i === selectedBox ? { ...box, label: label.trim() } : box
      ));
      setLabel('');
    }
  };

  const handleDelete = () => {
    if (selectedBox !== null) {
      setAnnotations(prev => prev.filter((_, i) => i !== selectedBox));
      setSelectedBox(null);
      setLabel('');
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4" ref={containerRef}>
      <div className="mb-4 flex gap-4">
        <form onSubmit={handleLabelSubmit} className="flex gap-2">
          <input
            type="text"
            value={label}
            onChange={handleLabelChange}
            placeholder="Enter label"
            className="border p-2 rounded"
          />
          <button 
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            disabled={selectedBox === null}
          >
            Add Label
          </button>
        </form>
        <button 
          onClick={handleDelete}
          className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
          disabled={selectedBox === null}
        >
          Delete Box
        </button>
      </div>
      <canvas
        ref={canvasRef}
        width={800}
        height={600}
        className="border border-gray-300 cursor-crosshair"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      />
      <div className="mt-4 text-sm text-gray-600">
        Click and drag to draw boxes. Select a box and enter a label to annotate it.
      </div>
    </div>
  );
};

export default ImageAnnotator;
