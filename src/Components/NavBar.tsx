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

class NavBar extends React.Component {
    render() {
        return(
            <div>
                <Navbar>
                    <NavbarBrand href="/">ZotScheduler</NavbarBrand>
                    <Nav className="m1-auto">
                        <NavItem>
                            <NavLink>Course Search</NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink>Scheduler</NavLink>
                        </NavItem>
                    </Nav>
                </Navbar>
            </div>
        );
    }
}

export default NavBar;