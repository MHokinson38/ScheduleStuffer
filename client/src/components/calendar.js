import React, {Component} from 'react';
import {DayPilotCalendar} from "@daypilot/daypilot-lite-react";

class Calendar extends Component {

    constructor(props) {
        super(props);
        this.state = {
            viewType: "Resources",
            columns: [
                { name: "Monday", id: "m"},
                { name: "Tuesday", id: "t"},
                { name: "Wednesday", id: "w"},
                { name: "Thursday", id: "th"},
                { name: "Friday", id: "f"}
            ]
        };
    }

  render() {
    const {...config} = this.state;

    return (
      <div>
        <DayPilotCalendar {...config} />
      </div>
    );
  }
}

export default Calendar;