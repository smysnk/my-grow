import logo from './logo.svg';
import './App.css';
import useStatus from './hooks/useStatus';

var ws = new WebSocket("ws://192.168.0.131");

ws.onopen = function () {
  ws.send("Hello");
};

window.ws = ws;

function App() {

  const { data } = useStatus(ws);
  
  return (
    <div className="App">
      <header className="App-header">
        
        <div className="code">{ JSON.stringify(data, null, 2) }</div>
       
      </header>
    </div>
  );
}

export default App;
