import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';


class Nav extends React.Component {
    renderCharacters() {
        const characters = this.props.characters;
        const active = this.props.active;
        const onClick = this.props.onClick;
        const rows = []
        for(let i=0;i<characters.length;i++) {
            let buttonClass = (characters[i]["name"] === active) ? "active" : "";
            rows.push(<li key={i}><button id={buttonClass} onClick={onClick}>{characters[i]["name"]}</button></li>);
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
        const { data } = this.state;
        if (Object.keys(data).length === 0) {
            return <h1> Data is Loading, please stand by... </h1>;
        }
        return (
            <React.Fragment>
            <Nav characters = {this.state.data["characters"]} active = {this.state.active} onClick={button => this.setState({active: button.target.innerText})}/>
            </React.Fragment>
        );
    }
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<WealthViewer/>);
