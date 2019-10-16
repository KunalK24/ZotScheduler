import * as React from 'react';
import { Component } from 'react';
import CourseSearchBar from './CourseSearchBar';
import ResultsCard from './ResultsCard';

export interface State {
    courseCode : string
}

class SearchScreen extends React.Component< {}, State> {
    constructor(props : any) {
        super(props);
        this.state = {
            courseCode : ""
        }
        this.handleCourseCodeChange = this.handleCourseCodeChange.bind(this);
    }

    handleCourseCodeChange(courseCode : string) {
        this.setState({courseCode : courseCode})
    }


    render() {
        return(
            <div>
                <h1>Course Search</h1>
                <CourseSearchBar 
                    courseCode={this.state.courseCode} 
                    onCourseCodeChange={this.handleCourseCodeChange}>
                </CourseSearchBar>
                <ResultsCard>{this.state.courseCode}</ResultsCard>
            </div>
        );
    }
}

export default SearchScreen;