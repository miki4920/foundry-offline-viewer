import React from 'react';
import ReactDOM from 'react-dom/client';

import {v4 as uuidv4} from 'uuid';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import {Bar} from 'react-chartjs-2';

import './index.css';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

const md5 = require('md5')


class Nav extends React.Component {
    renderCharacters() {
        const rows = []
        for (let i = 0; i < this.props.data.length; i++) {
            let buttonClass = (this.props.data[i]["name"] === this.props.active) ? "active" : "";
            rows.push(<li key={uuidv4()}>
                <button className={buttonClass} onClick={this.props.onClick}>{this.props.data[i]["name"]}</button>
            </li>);
        }
        rows.push(<li key={uuidv4()}>
            <button onClick={this.props.refreshData}>Refresh Data</button>
        </li>)
        return rows
    }

    render() {
        const rows = this.renderCharacters()
        return (
            <React.Fragment>
                <nav>
                    <div id="sticky_nav">
                        <header>Wealth</header>
                        <header>Manager</header>
                        <ul>
                            {rows}

                        </ul>
                    </div>
                </nav>
            </React.Fragment>
        );
    }
}

class Graphs extends React.Component {
    constructor(props) {
        super(props);
        this.options = {
            responsive: true,
            onClick: this.graphClickEvent(this.props.updateActive)
        }
    }

    graphClickEvent(updateActive) {
        return function onClick(event) {
            const points = event["chart"].getElementsAtEventForMode(event, 'nearest', {intersect: true}, true)
            if (points.length) {
                const firstPoint = points[0]
                const label = event["chart"].data.labels[firstPoint.index];
                updateActive(label)
            }

        }
    }

    wealth(items) {
        return items.reduce((total, item) => total + parseFloat(item["total"]), 0)
    }

    wealthWithoutConsumables(items) {
        let consumableOrZero = n => n["consumable"] ? 0 : parseFloat(n["total"])
        return items.reduce((a, b) => a + consumableOrZero(b), 0)
    }

    hashColor(label) {
        return '#' + md5(label).slice(10, 16);
    }

    getGraphData(data, valueFunction) {
        const graphList = [];
        const graphData = {};
        for (let i = 0; i < data.length; i++) {
            let borderColor = this.hashColor(data[i]["name"])
            let backgroundColor = borderColor + "40"
            graphList.push([data[i]["name"], valueFunction(data[i]["items"]), borderColor, backgroundColor])
        }
        graphList.sort((a, b) => b[1] - a[1])
        graphData["labels"] = []
        graphData["data"] = []
        graphData["borderColor"] = []
        graphData["backgroundColor"] = []
        for (const element of graphList) {
            graphData["labels"].push(element[0])
            graphData["data"].push(element[1])
            graphData["borderColor"].push(element[2])
            graphData["backgroundColor"].push(element[3])
        }
        return graphData
    }


    graph(graphData, label) {
        console.log(graphData["borderColor"] + "33")
        return {
            labels: graphData["labels"],
            datasets: [{
                label: label,
                data: graphData["data"],
                backgroundColor: graphData["backgroundColor"],
                borderColor: graphData["borderColor"],
                borderWidth: 1
            }]
        }
    }

    render() {
        const wealth = this.getGraphData(this.props.data, this.wealth)
        const wealthGraph = this.graph(wealth, "Wealth in GP")
        const wealthWithoutConsumables = this.getGraphData(this.props.data, this.wealthWithoutConsumables)
        const wealthWithoutConsumablesGraph = this.graph(wealthWithoutConsumables, "Wealth in GP without consumables")
        return <React.Fragment>
            <div className="chart">
                <Bar options={this.options} data={wealthGraph} type="bar"/>
            </div>
            <div className="chart">
                <Bar options={this.options} data={wealthWithoutConsumablesGraph} type="bar"/>
            </div>
        </React.Fragment>
    }
}


class Table extends React.Component {
    tableHeader = ["name", "level", "quantity", "value", "total", "consumable"]

    capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    renderHeaderRow() {
        const rows = []
        for (const header of this.tableHeader) {
            let buttonClass = "";
            if (header === this.props.sorting) {
                buttonClass = "active"
                if (isNaN(this.props.data[0]["items"][0][header])) {
                    buttonClass += this.props.ascending ? " headerSortAscending" : " headerSortDescending"
                } else {
                    buttonClass += this.props.ascending ? " headerSortAscendingNumber" : " headerSortDescendingNumber"
                }

            }
            rows.push(<th key={uuidv4()} className="tableHeader">
                <button onClick={this.props.onClick}
                        className={buttonClass}>{this.capitalizeFirstLetter(header)}</button>
            </th>)
        }
        return (
            <React.Fragment key={uuidv4()}>
                <tr key={uuidv4()}>
                    {rows}
                </tr>
            </React.Fragment>
        )
    }

    renderRow(item) {
        return (
            <React.Fragment key={uuidv4()}>
                <tr key={uuidv4()}>
                    <th key={uuidv4()}><p>{item["name"]}</p></th>
                    <th key={uuidv4()}><p>{item["level"]}</p></th>
                    <th key={uuidv4()}><p>{item["quantity"]}</p></th>
                    <th key={uuidv4()}><p>{item["value"]} GP</p></th>
                    <th key={uuidv4()}><p>{item["total"]} GP</p></th>
                    <th key={uuidv4()}><p>{item["consumable"] ? "✓" : '✗'}</p></th>
                </tr>
            </React.Fragment>
        )
    }

    compareFct(a, b) {
        a = a[this.props.sorting]
        b = b[this.props.sorting]
        const flip = this.props.ascending ? 1 : -1
        let value;
        if (isNaN(a)) {
            if (isNaN(b)) {
                value = a.localeCompare(b);
            } else {
                value = 1;
            }
        } else {
            if (isNaN(b)) {
                value = -1;
            } else {
                value = parseFloat(a) - parseFloat(b);
            }
        }
        return value * (flip)
    }

    renderRows() {
        const rows = []
        rows.push(this.renderHeaderRow())
        for (let i = 0; i < this.props.data.length; i++) {
            if (this.props.data[i]["name"] === this.props.active) {
                let items = this.props.data[i]["items"]
                items = items.sort((a, b) => this.compareFct(a, b))
                for (let itemIndex = 0; itemIndex < items.length; itemIndex++) {
                    rows.push(this.renderRow(items[itemIndex], itemIndex));
                }
            }
        }
        return rows
    }

    render() {
        return (
            <React.Fragment>
                <table>
                    <tbody>
                    {this.renderRows()}
                    </tbody>
                </table>
            </React.Fragment>);
    }

}


class WealthViewer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: {},
            active: "",
            sorting: "name",
            ascending: true
        }
    }

    getData() {
        fetch(
            "https://wealth-viewer.herokuapp.com/wealth")
            .then((res) => res.json())
            .then((data) => {
                this.setState({
                    data: data,
                    active: data[0]["name"]
                });
            })
    }

    componentDidMount() {
        this.getData()
    }

    sortTable(button) {
        const text = button.target.innerText.toLowerCase()
        if (text === this.state.sorting) {
            this.setState({ascending: !this.state.ascending})
        } else {
            this.setState({
                sorting: text,
                ascending: true
            })
        }
    }

    render() {
        if (Object.keys(this.state.data).length === 0) {
            return <h1> Data is Loading, please stand by... </h1>;
        }
        return (
            <React.Fragment>
                <Nav data={this.state.data} active={this.state.active}
                     onClick={button => this.setState({active: button.target.innerText})}
                     refreshData={() => this.getData()}/>
                <main>
                    <header>{this.state.active}</header>
                    <div id="charts">
                        <Graphs data={this.state.data} updateActive={(label) => this.setState({active: label})}/>
                    </div>
                    <section id="table">
                        <Table data={this.state.data} active={this.state.active}
                               sorting={this.state.sorting} ascending={this.state.ascending}
                               onClick={(button) => {
                                   this.sortTable(button)
                               }}/>
                    </section>
                </main>
            </React.Fragment>
        );
    }
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<WealthViewer/>);
