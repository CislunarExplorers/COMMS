import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      commands: [],
      isLoading: false
    };
  }

  componentDidMount() {
    this.setState({ isLoading: true });

  fetch("http://localhost:5000/commands"
   ).then(response => response.json())
    .then(commands => this.setState({ commands: commands.commands, isLoading: false }));
  }

  handleSubmit(event) {
    alert('A name was submitted: ' + this.state.value);
    event.preventDefault();
  }

  render() {
    const { commands, isLoading } = this.state;
    if(isLoading){
      return <p>Loading...</p>
    }
    console.log(commands)
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Cislunar Explorers</h1>
        </header>
        <p className="App-intro">
          Press submit to send commands to the Satellite.
        </p>
        
        <form id = "form_commands" onSubmit={this.handleSubmit}>
         {commands.map(function(listValue){
            return (<div> 
              {listValue} :  <input type="text"></input> <br /><br />
              </div>)
          })}

         <input type="submit" value="Submit" />
        </form>

      </div>
    );
  }
}

export default App;
