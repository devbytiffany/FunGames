import {useState} from 'react';
import './App.css';
import Square from './components/Square';
import Board from './components/Board';

function App() {
  const [player, setPlayer] = useState ('X');

  function changePlayer(){
    if (player ==='X'){
      setPlayer('O')
    } else{
      setPlayer('X')
    }
  }
  return  ( 
    <>
      <h1>Curren Player: {player}</h1>
      <button onClick={changePlayer}>Change Player</button>
      <Board  />
    </>
  );
}


export default App;