import * as React from 'react';
import { Component } from 'react';
import NavBar from './NavBar';
import SearchScreen from './SearchScreen';

export interface Props {

}

export interface State {
    showSearchScreen : boolean
}
class MainScreen extends React.Component<Props, State>{
    constructor(props : any){
        super(props)
        this.state = {
            showSearchScreen : true,
        }

        this.handleSearchScreenChange = this.handleSearchScreenChange.bind(this)
        this.handleSchedulerScreenChange = this.handleSchedulerScreenChange.bind(this)
    }

    handleSearchScreenChange() {
        this.setState({showSearchScreen : true})
    }
    
    handleSchedulerScreenChange() {
        this.setState({showSearchScreen : false})
    }

    render() {
        return(
            <div>
                <NavBar 
                    onSearchScreenChange={this.handleSearchScreenChange}
                    onSchedulerScreenChange={this.handleSchedulerScreenChange}>
                </NavBar>
                <SearchScreen showSearchScreen={this.state.showSearchScreen}></SearchScreen>
            </div>
        );
    }
}