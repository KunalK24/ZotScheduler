import React from 'react';
import logo from './logo.svg';
import './App.css';
import NavBar from "./Components/NavBar"
import SearchScreen from "./Components/SearchScreen"

function App() {
  return (
    <div className="App">
      <NavBar></NavBar>
      <SearchScreen></SearchScreen>
    </div>
  );
}

export default App;
