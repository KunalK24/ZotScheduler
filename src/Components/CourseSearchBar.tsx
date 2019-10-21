import * as React from 'react';
import axios from 'axios';
import { Component } from 'react';
import { 
    Button, 
    Form, 
    Label, 
    Input } from 'reactstrap';

export interface Props {
    courseCode : string,
    onCourseCodeChange : any,
    onCourseSubmit : any
}

class CourseSearchBar extends React.Component<Props> {
    constructor(props : any){
        super(props);

        this.handleSubmit = this.handleSubmit.bind(this)
        this.handleCourseCodeChange = this.handleCourseCodeChange.bind(this)
    }

    handleSubmit = () => {
        this.props.onCourseSubmit()
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
                    placeholder="I&C SCI 90 ..."
                    value={this.props.courseCode}
                    onChange={this.handleCourseCodeChange}
                />
                <Button type="button" className="primary m-2" onClick={this.handleSubmit}>Submit</Button>
            </Form>
        );
    }
}

export default CourseSearchBar;