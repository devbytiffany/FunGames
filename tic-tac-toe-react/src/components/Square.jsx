export default function Square({ value, onSquareClick, isWinningSquare }) {
  return (
    <button
      className={`square ${isWinningSquare ? 'highlighted' : ''}`}
      onClick={onSquareClick}
    >
      {value}
    </button>
  );
}