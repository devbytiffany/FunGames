import { useState } from 'react';
import Square from './Square';
import './App.css';

function Scoreboard({ xWins, oWins, ties }) {
  return (
    <div className="scoreboard">
      <div className="score-box">
        <span className="score-label">Player X</span>
        <span className="score-value">{xWins}</span>
      </div>
      <div className="score-box">
        <span className="score-label">Ties</span>
        <span className="score-value">{ties}</span>
      </div>
      <div className="score-box">
        <span className="score-label">Player O</span>
        <span className="score-value">{oWins}</span>
      </div>
    </div>
  );
}

export default function Board() {
  const [squares, setSquares] = useState(Array(9).fill(null));
  const [xIsNext, setXIsNext] = useState(true);
  const [xWins, setXWins] = useState(0);
  const [oWins, setOWins] = useState(0);
  const [ties, setTies] = useState(0);

  const winInfo = calculateWinner(squares);
  const winner = winInfo ? winInfo.winner : null;
  const winningLine = winInfo ? winInfo.line : [];

  function handleClick(index) {
    if (squares[index] !== null || winner) {
      return;
    }
    const nextSquares = squares.slice();
    if (xIsNext) {
      nextSquares[index] = "X";
    } else {
      nextSquares[index] = "O";
    }

    const nextWinInfo = calculateWinner(nextSquares);
    if (nextWinInfo) {
      if (nextWinInfo.winner === "X") {
        setXWins(xWins + 1);
      } else {
        setOWins(oWins + 1);
      }
    } else if (!nextSquares.includes(null)) {
      setTies(ties + 1);
    }

    setSquares(nextSquares);
    setXIsNext(!xIsNext);
  }

  function handleRestart() {
    setSquares(Array(9).fill(null));
    setXIsNext(true);
  }

  let status;
  if (winner) {
    status = "Winner: " + winner;
  } else if (!squares.includes(null)) {
    status = "Game ended in a draw!";
  } else {
    status = "Next player: " + (xIsNext ? "X" : "O");
  }

  return (
    <div className="game-container">
      <Scoreboard xWins={xWins} oWins={oWins} ties={ties} />
      <div className="status">{status}</div>
      <div className="board-grid">
        {squares.map((value, index) => (
          <Square
            key={index}
            value={value}
            onSquareClick={() => handleClick(index)}
            isWinningSquare={winningLine.includes(index)}
          />
        ))}
      </div>
      <button className="restart-button" onClick={handleRestart}>
        Restart Game
      </button>
    </div>
  );
}

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return {
        winner: squares[a],
        line: lines[i]
      };
    }
  }
  return null;
}