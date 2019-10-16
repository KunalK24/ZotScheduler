import * as React from 'react';
import axios from 'axios';
import { Component } from 'react';
import { Button, Form, Label, Input } from 'reactstrap';

const CORSFix = "https://cors-anywhere.herokuapp.com/";
const baseURL = "http://catalogue.uci.edu/search/?P="

export interface Props {
    courseCode : string,
    onCourseCodeChange : any
}

class CourseSearchBar extends React.Component<Props> {
    constructor(props : any){
        super(props);

        this.handleSubmit = this.handleSubmit.bind(this)
        this.handleCourseCodeChange = this.handleCourseCodeChange.bind(this)
    }

    handleSubmit = (e : any) => {
        axios.get(CORSFix.concat(baseURL, this.props.courseCode))
        .then(response => {
            console.log(response.data)
        })
        .catch(error => {
            alert("Error Code: " + error);
            
        })
    }

    handleCourseCodeChange = (e : any) => {
        this.props.onCourseCodeChange(e.target.value)
    }

    render() {
        return (
            <Form inline>
                <Label className="mr-sm-2">Course Name</Label>
                <Input 
                    type="text" 
                    name="courseCode"
                    placeholder="EECS 10..."
                    value={this.props.courseCode}
                    onChange={this.handleCourseCodeChange}
                />
                <Button type="button" className="primary" onClick={this.handleSubmit}>Submit</Button>
            </Form>
        );
    }
}

export default CourseSearchBar;