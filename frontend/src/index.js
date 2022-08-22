import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
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

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);


class Nav extends React.Component {
    renderCharacters() {
        const rows = []
        for (let i = 0; i < this.props.data.length; i++) {
            let buttonClass = (this.props.data[i]["name"] === this.props.active) ? "active" : "";
            rows.push(<li key={uuidv4()}>
                <button className={buttonClass} onClick={this.props.onClick}>{this.props.data[i]["name"]}</button>
            </li>);
        }
        return rows
    }

    render() {
        const rows = this.renderCharacters()
        return (
            <React.Fragment>
                <nav>
                    <div id="sticky_nav">
                        <header>Wealth Manager</header>
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
    options = {
        responsive: true,
        maintainAspectRatio: false
    }
    // TODO: CHANGE COLOURS UPON CONVERTING TO FOUNDRY 10
    characterColours = ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)', 'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)', 'rgba(199, 160, 190, 0.2)']

    wealth(items) {
        return items.reduce((total, item) => total + parseFloat(item["total"]), 0)
    }

    wealthWithoutConsumables(items) {
        let consumableOrZero = n => n["consumable"] ? 0 : parseFloat(n["total"])
        return items.reduce((a, b) => a + consumableOrZero(b), 0)
    }

    getGraphData(data, valueFunction) {
        const graphList = [];
        const graphData = {};
        for (let i = 0; i < data.length; i++) {
            graphList.push([data[i]["name"], valueFunction(data[i]["items"]), this.characterColours[i]])
        }
        graphList.sort((a, b) => b[1] - a[1])
        graphData["labels"] = []
        graphData["data"] = []
        graphData["backgroundColor"] = []
        for (const element of graphList) {
            graphData["labels"].push(element[0])
            graphData["data"].push(element[1])
            graphData["backgroundColor"].push(element[2])
        }
        return graphData
    }

    graph(graphData, label) {
        return {
            labels: graphData["labels"],
            datasets: [{
                label: label,
                data: graphData["data"],
                backgroundColor: graphData["backgroundColor"],
                borderColor: graphData["backgroundColor"].map((x) => x.replace("0.2", "1")),
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
            <Bar options={this.options} data={wealthGraph} type="bar"/>
            <Bar options={this.options} data={wealthWithoutConsumablesGraph} type="bar"/>
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
                if(isNaN(this.props.data[0]["items"][0][header])) {
                    buttonClass += this.props.ascending ? " headerSortAscending" : " headerSortDescending"
                }
                else {
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

    componentDidMount() {
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
                     onClick={button => this.setState({active: button.target.innerText})}/>
                <main>
                    <header>{this.state.active}</header>
                    <section id="charts">
                        <Graphs data={this.state.data}/>
                    </section>
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
