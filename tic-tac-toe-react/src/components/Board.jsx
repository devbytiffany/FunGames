import Square from "./Square";

function Board() {
    const squares=Array.from({length : 9}, (value, index) => index +1);
  return (
    <div className ="board-grid">
        {squares.map((value, index)=>{
           return <Square key={index} value={value} /> 
        })}
    </div>
  );
}

export default Board;