import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { v4 as uuidv4 } from 'uuid';

class Nav extends React.Component {
    renderCharacters() {
        const characters = this.props.characters;
        const active = this.props.active;
        const onClick = this.props.onClick;
        const rows = []
        for (let i = 0; i < characters.length; i++) {
            let buttonClass = (characters[i]["name"] === active) ? "active" : "";
            rows.push(<li key={uuidv4()}>
                <button id={buttonClass} onClick={onClick}>{characters[i]["name"]}</button>
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


class Table extends React.Component {
    renderHeaderRow(data) {
        return (
            <React.Fragment key={uuidv4()}>
                <tr key={uuidv4()}>
                    <th key={uuidv4()} className="row_header"><p>Name</p></th>
                    <th key={uuidv4()} className="row_header"><p>Level</p></th>
                    <th key={uuidv4()} className="row_header "><p>Quantity</p></th>
                    <th key={uuidv4()} className="row_header "><p>Value</p></th>
                    <th key={uuidv4()} className="row_header "><p>Total Value</p></th>
                    <th key={uuidv4()} className="row_header "><p>Consumable</p></th>
                </tr>
            </React.Fragment>
        )
    }

    renderRow(item, itemKey) {
        return (
            <React.Fragment key={uuidv4()}>
                <tr key={uuidv4()}>
                    <th key={uuidv4()}><p>{item["name"]}</p></th>
                    <th key={uuidv4()}><p>{item["level"]}</p></th>
                    <th key={uuidv4()}><p>{item["quantity"]}</p></th>
                    <th key={uuidv4()}><p>{item["value"]} GP</p></th>
                    <th key={uuidv4()}><p>{item["value"] * item["quantity"]} GP</p></th>
                    <th key={uuidv4()}><p>{item["consumable"] ? "✓" : '✗'}</p></th>
                </tr>
            </React.Fragment>
        )
    }

    renderRows(characters, active) {
        const rows = []
        rows.push(this.renderHeaderRow())
        for (let i = 0; i < characters.length; i++) {
            if (characters[i]["name"] === active) {
                const items = characters[i]["items"]
                for (let itemIndex = 0; itemIndex < items.length; itemIndex++) {
                    rows.push(this.renderRow(items[itemIndex], itemIndex));
                }
            }
        }
        return rows
    }

    render() {
        const characters = this.props.characters;
        const active = this.props.active;
        return (
            <React.Fragment>
                <table>
                    <tbody>
                    {this.renderRows(characters, active)}
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
            active: ""
        }
    }

    componentDidMount() {
        fetch(
            "http://localhost:5000/wealth")
            .then((res) => res.json())
            .then((json) => {
                this.setState({
                    data: json,
                    active: json["characters"][0]["name"]
                });
            })
    }

    render() {
        const {data} = this.state;
        if (Object.keys(data).length === 0) {
            return <h1> Data is Loading, please stand by... </h1>;
        }
        return (
            <React.Fragment>
                <Nav characters={this.state.data["characters"]} active={this.state.active}
                     onClick={button => this.setState({active: button.target.innerText})}/>
                <main>
                    <Table characters={this.state.data["characters"]} active={this.state.active}/>
                </main>
            </React.Fragment>
        );
    }
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<WealthViewer/>);
