import * as React from 'react';
import './ResultCard.css'
import cheerio from 'cheerio';
import { Component } from 'react';
import { 
    Card, 
    CardText, 
    CardHeader, 
    CardBody, 
    Col} from 'reactstrap';

export interface Props {
    courseInfo : string,
    courseCode : string
}

export interface State {
    courseNumber : string,
    courseTitle : string,
    units : string
}

class ResultsCard extends React.Component<Props, State> {
    constructor(props : any) {
        super(props)
        this.state = {
            courseNumber : '',
            courseTitle : '',
            units: '',
        }
    }

    componentDidMount() {
        this.parseWebpage()
    }

    parseWebpage() {
        const cheerio = require('cheerio')
        const $ = cheerio.load(this.props.courseInfo)
        const title = $('div.searchresult.search-courseresult').text()
        const course = title.split('.')
        this.setState({courseNumber : course[0]})
        this.setState({courseTitle : course[1]})
        this.setState({units : course[2]})
    
    }

    render() {
        return(
            <div>
                <Col sm="4">
                    <Card className="Card">
                        <CardHeader className="CardHeader">{this.props.courseCode}</CardHeader>
                        <CardBody>
                            <CardText>{this.state.courseNumber}</CardText>
                            <CardText>{this.state.courseTitle}</CardText>
                            <CardText>{this.state.units}</CardText>
                        </CardBody>
                    </Card>
                </Col>
            </div>
        );
    }
}

export default ResultsCard;