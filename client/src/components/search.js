// Purpose: Search form for looking through courses 
// Allow user to specify the semester, course subject, number (optionally)
// Probably change number to be a dropdown of level (i.e. 100, 200, 300, 400, 500)

import React, { useState } from "react";

//=======================
// SearchForm Component 
//=======================
function SearchForm() {
    const [classSearch, setClassSearch] = useState({
        semester: "fall",
        year: "2023",
        subject: "CS",
        number: "1xx"
    });

    function onSubmitSearch(e) {
        e.preventDefault();
        console.log(`Submitting search for course: ${classSearch.semester} ${classSearch.year} ${classSearch.subject} ${classSearch.number}`);
    
        submitSearchGQLRequest(classSearch, (res) => {console.log(res)});
    }

    // Return form with input fields for semester, year, subject, number (optional), all as text 
    // and a submit button.
    return <div className="App">
        <header className="App-header">
            <form onSubmit={onSubmitSearch}>
                <label>
                    Year:
                    <input 
                        type="text"
                        defaultValue="2023"
                        onChange={({ target }) =>
                            setClassSearch({ ...classSearch, year: target.value })
                        }>
                    </input>
                </label>
                <label>
                    Semester: 
                    <select
                        onChange={({ target }) =>
                            setClassSearch({ ...classSearch, semester: target.value })
                        }
                    >
                        <option value="fall" defaultValue>Fall</option>
                        <option value="spring">Spring</option>
                    </select>
                </label>
                <label>
                    Subject:{" "}
                    <input
                        type="text"
                        defaultValue="CS"
                        onChange={({ target }) =>
                            setClassSearch({ ...classSearch, subject: target.value })
                        }
                    />
                </label>
                <label>
                    Course Number:{" "}
                    <select
                        onChange={({ target }) =>
                            setClassSearch({ ...classSearch, semester: target.value })
                        }
                    >
                        <option value="1xx" defaultValue>1--</option>
                        <option value="2xx">2--</option>
                        <option value="3xx">3--</option>
                        <option value="4xx">4--</option>
                        <option value="5xx">5--</option>
                    </select>
                </label>
                <input type="submit" value="Search" />
            </form>
        </header>
    </div>
}

//========================
// Search Functionality 
// GQL Query submission and input cleaning 
//========================
/**
 * Sanitize text inputs of the search form to ensure following restrictions: 
 * Year: 4 digits
 * Course: Value alpha subject code 
 * Note* Course number and subject are fixed dropdowns
 * 
 * @param {Obj} input - See SearchForm component classSearch state  
 * 
 * @returns {Obj} - Sanitized input
 */
function sanitizeAndValidate(input) {
    // Remove whitespace and verify that year is 4 numeric digits, and above 2000
    let year = input.year.trim();
    let year_regex = /^\d{4}|^\d{2}$/; // Either two or four digits 
    if (year_regex.test(year) && year >= 2000) {
        if (year.length === 2) {
            year = "20" + year;
        }

        input = { ...input, year: year };
    }
    else {
        return null;
    }

    // Verify subject is only alpha characters, at least two characters 
    let subject = input.subject.trim();
    let subject_regex = /^[a-zA-Z]+$/;
    if (subject_regex.test(subject) && subject.length >= 2) {
        input = { ...input, subject: subject.toUpperCase() };
    }
    else {
        return null;
    }

    return input;
}

function submitSearchGQLRequest(input, resHandler) {
    // Sanitize the raw input 
    input = sanitizeAndValidate(input);
    if (input === null) {
        return null;
    }

    // Construct the GQL query
    let query = `query CourseInfo($year: String! 
                                $semester: String! 
                                $subjectCode: String!
                                $courseNumber: String!) 
    {
        courseInfo(year: $year, 
                semester: $semester, 
                subjectCode: $subjectCode, 
                courseNumber: $courseNumber) 
        { 
            label 
            sections {
                sectionNumber
                enrollmentStatus
                meetings {
                    isOnline
                    start
                    end
                    daysOfWeek
                    roomNumber
                    buildingName
                }            
            }
        }
    }`;
    let year = input.year;
    let semester = input.semester;
    let subjectCode = input.subject;
    let courseNumber = input.number;

    fetch('/graphql', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          query,
          variables: { year, semester, subjectCode, courseNumber },
        })
    })
    .then(r => r.json())
    .then(r => resHandler(r));
}

export default SearchForm;