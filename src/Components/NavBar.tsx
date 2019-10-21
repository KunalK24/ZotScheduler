import * as React from 'react';
import { Component } from 'react';
import {
    Collapse,
    Navbar,
    NavbarToggler,
    NavbarBrand,
    Nav,
    NavItem,
    NavLink } from 'reactstrap';

export interface Props {
    onSearchScreenChange : any
    onSchedulerScreenChange : any
}

export interface State {

}

class NavBar extends React.Component<Props, State>{
    constructor(props : any){
        super(props)

        this.handleSearchScreenChange = this.handleSearchScreenChange.bind(this)
        this.handleSchedulerScreenChange = this.handleSchedulerScreenChange.bind(this)
    }

    handleSearchScreenChange() {
        console.log("Hello")
    }

    handleSchedulerScreenChange() {
        console.log("HI")
    }

    render() {
        return(
            <div>
                <Navbar>
                    <NavbarBrand href="/">ZotScheduler</NavbarBrand>
                    <Nav className="m1-auto">
                        <NavItem>
                            <NavbarToggler onClick={this.handleSearchScreenChange}>Course Search</NavbarToggler>
                        </NavItem>
                        <NavItem>
                            <NavbarToggler onClick={this.handleSchedulerScreenChange}>Scheduler</NavbarToggler>
                        </NavItem>
                    </Nav>
                </Navbar>
            </div>
        );
    }
}

export default NavBar;