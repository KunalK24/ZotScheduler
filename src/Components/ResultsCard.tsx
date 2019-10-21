import * as React from 'react';
import { Component } from 'react';
import { 
    Card, 
    CardText, 
    CardHeader, 
    CardBody } from 'reactstrap';

export interface Props {
    courseInfo : string,
    courseCode : string
}
class ResultsCard extends React.Component<Props> {
    constructor(props : any) {
        super(props)
    }

    render() {
        return(
            <div>
                <Card>
                    <CardHeader>{this.props.courseCode}</CardHeader>
                    <CardBody>
                        <CardText>{this.props.courseInfo}</CardText>
                    </CardBody>
                </Card>
            </div>
        );
    }
}

export default ResultsCard;