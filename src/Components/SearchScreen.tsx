import * as React from 'react';
import { Component } from 'react';
import CourseSearchBar from './CourseSearchBar';
import ResultsCard from './ResultsCard';
import axios from 'axios';
import { Button } from 'reactstrap';


const CORSFix = "https://cors-anywhere.herokuapp.com/";
const baseURL = "http://catalogue.uci.edu/search/?P=";


export interface Props {
    showSearchScreen : boolean
}

export interface State {
    courseCode : string,
    courseInfo : string,
    showResults : boolean
}

class SearchScreen extends React.Component< Props, State> {
    constructor(props : any) {
        super(props);
        this.state = {
            courseCode : "",
            courseInfo : "",
            showResults : false
        }
        this.handleCourseCodeChange = this.handleCourseCodeChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    handleCourseCodeChange(courseCode : string) {
        this.setState({courseCode : courseCode})
    }

    handleSubmit(e : any) {
        axios.get(CORSFix.concat(baseURL, this.state.courseCode))
        .then(response => {
            this.setState({courseInfo : response.data})
            this.setState({showResults : true})
        })
        .catch(error => {
            this.setState({courseInfo : "No results found! Try again"})
            alert("Error Code: " + error);
        })
    }

    render() {
        return(
            <div>
                <h1>Course Search</h1>
                <CourseSearchBar 
                    courseCode={this.state.courseCode} 
                    onCourseCodeChange={this.handleCourseCodeChange}
                    onCourseSubmit={this.handleSubmit}>
                </CourseSearchBar>
                {this.state.showResults 
                    ? (<ResultsCard 
                        courseInfo={this.state.courseInfo}
                        courseCode={this.state.courseCode}>
                        </ResultsCard>)
                    : (<p>{this.state.courseInfo}</p>)}
            </div>
        );
    }
}

export default SearchScreen;