var styles = require('./style.css');
var React = require('react');
var ReactDOM = require('react-dom');
var $ = require('jquery');

var Loading = React.createClass({
  render: function() {
    return (
      <div className={styles.loading}>
        <p>
          Ваш запрос обрабатывается на сервере.
          Пожалуйста подождите и не закрывайте вкладку.
        </p>
        <div className={styles.loader}>
          <span className={styles.dot + ' ' + styles.dot1}></span>
          <span className={styles.dot + ' ' + styles.dot2}></span>
          <span className={styles.dot + ' ' + styles.dot3}></span>
          <span className={styles.dot + ' ' + styles.dot4}></span>
        </div>
      </div>
    );
  }
});

var Result = React.createClass({
  render: function() {
    let childs = this.props.data.map(function(book) {
      return (
        <div key={book.name}>
        <p>{book.name}</p>
        <p>{book.result}</p>
        </div>
      );
    });
    return (
      <div className={styles.contentBox}>
      <button onClick={this.props.back}>Back</button>
      <br />
      {childs}
      </div>
    );
  }
});

var File = React.createClass({
  getInitialState: function() {
    return {files: {length: 0}, error: false};
  },
  componentDidMount: function() {
    this.setState({error: this.props.error})
  },
  handleSubmit: function() {
    if (this.state.files.length == 0) {
      this.setState({error: true})
      return false;
    }
    var data = new FormData();
    $.each(this.state.files, function(key, value)
    {
        data.append(key, value);
    });
    this.props.startLoading(true);
    $.ajax({
        url: 'submitfiles',
        type: 'POST',
        data: data,
        cache: false,
        dataType: 'json',
        processData: false, // Don't process the files
        contentType: false, // Set content type to false as jQuery will tell the server its a query string request
        success: function(data, textStatus, jqXHR) {
            if(typeof data.error === 'undefined')
            {
                // Success so call function to process the form
                this.props.onFormSubmit(data);
            }
            else
            {
                // Handle errors here
                this.props.startLoading(false);
                console.log('ERRORS: ' + data.error);
            }
        }.bind(this),
        error: function(jqXHR, textStatus, errorThrown) {
            // Handle errors here
            this.props.startLoading(false);
            // STOP LOADING SPINNER
        }.bind(this)
    });
    return false;
  },
  handleChange: function(e) {
    this.setState({files: e.target.files})
  },
  render: function() {
    let error = <span />
    if (this.state.error) {
      error = <span className={styles.error} >Форма заполнена неправильно, либо сервер недоступен</span>
    }
    return (
      <div className={styles.contentBox}>
        <div>
          Можно загрузить один или несколько файлов чистого текста
          (не pdf или html). Пока поддерживается только кодировка cp1251.
        </div>
        <input onChange={this.handleChange} multiple type="file"/>
        <button onClick={this.handleSubmit}>submit</button>
        <br />
        {error}
      </div>
    );
  }
});

var Archive = React.createClass({
  getInitialState: function() {
    return {files: {length: 0}, error: false};
  },
  componentDidMount: function() {
    this.setState({error: this.props.error})
  },
  handleSubmit: function() {
    if (this.state.files.length == 0) {
      this.setState({error: true})
      return false;
    }
    var data = new FormData();
    $.each(this.state.files, function(key, value)
    {
        data.append(key, value);
    });
    this.props.startLoading(true);
    $.ajax({
        url: 'submitarchive',
        type: 'POST',
        data: data,
        cache: false,
        dataType: 'json',
        processData: false, // Don't process the files
        contentType: false, // Set content type to false as jQuery will tell the server its a query string request
        success: function(data, textStatus, jqXHR) {
            if(typeof data.error === 'undefined')
            {
                // Success so call function to process the form
                this.props.onFormSubmit(data);
            }
            else
            {
                // Handle errors here
                this.props.startLoading(false);
                console.log('ERRORS: ' + data.error);
            }
        }.bind(this),
        error: function(jqXHR, textStatus, errorThrown) {
            // Handle errors here
            this.props.startLoading(false);
            // STOP LOADING SPINNER
        }.bind(this)
    });
    return false;
  },
  handleChange: function(e) {
    this.setState({files: e.target.files})
  },
  render: function() {
    let error = <span />
    if (this.state.error) {
      error = <span className={styles.error}>Форма заполнена неправильно, либо сервер недоступен</span>
    }
    return (
      <div className={styles.contentBox}>
        <div>
          Загрузите один архив с книгами. Все книги из архива будут обработаны.
          Поддерживаемые форматы:
        </div>
        <ul>
          <li> gztar </li>
          <li> bztar </li>
          <li> xztar </li>
          <li> tar </li>
          <li> zip </li>
        </ul>
        <input onChange={this.handleChange} type="file"/>
        <button onClick={this.handleSubmit}>submit</button>
        <br />
        {error}
      </div>
    );
  }
});

var Link = React.createClass({
  getInitialState: function() {
    return {link: "", error: false};
  },
  componentDidMount: function() {
    this.setState({error: this.props.error})
  },
  handleSubmit: function() {
    if (this.state.link == "") {
      this.setState({error: true})
      return false;
    }
    var data = {link: this.state.link};
    this.props.startLoading(true);
    $.ajax({
        url: 'submitlink',
        type: 'POST',
        data: JSON.stringify(data, null, '\t'),
        cache: false,
        dataType: 'json',
        success: function(data, textStatus, jqXHR) {
            if(typeof data.error === 'undefined')
            {
                // Success so call function to process the form
                this.props.onFormSubmit(data);
            }
            else
            {
                // Handle errors here
                this.props.startLoading(false);
                console.log('ERRORS: ' + data.error);
            }
        }.bind(this),
        error: function(jqXHR, textStatus, errorThrown) {
            // Handle errors here
            this.props.startLoading(false);
            // STOP LOADING SPINNER
        }.bind(this)
    });
    return false;
  },
  handleChange: function(e) {
    this.setState({link: e.target.value})
  },
  render: function() {
    let error = <span />
    if (this.state.error) {
      error = <span className={styles.error} >Форма заполнена неправильно, либо сервер недоступен</span>
    }
    return (
      <div className={styles.contentBox}>
        <div>
          Укажите ссылку на книгу. Желательно, чтоб там было как можно
          меньше лишних элементов. Рекомендуется сервис lib.ru
        </div>
        <input onChange={this.handleChange} type="text"/>
        <button onClick={this.handleSubmit}>submit</button>
        <br />
        {error}
      </div>
    );
  }
});

var App = React.createClass({
  getInitialState: function() {
    return {tab: "File", result: false, data: [], loading: false, error: false};
  },
  changeTab: function(tab) {
    this.setState({tab: tab, result: false, loading: false, error: false});
  },
  handleFormSubmit: function(result) {
    this.setState({result: true, data: result, loading: false, error: false});
  },
  render: function() {
    var tabs = {"File": {component: <File error={this.state.error} onFormSubmit={this.handleFormSubmit} startLoading={function(e) {this.setState({loading: e, error: !e})}.bind(this)} />, text: "Фаил"},
                "Archive": {component: <Archive error={this.state.error} onFormSubmit={this.handleFormSubmit} startLoading={function(e) {this.setState({loading: e, error: !e})}.bind(this)} />, text: "Архив"},
                "Link" :{component: <Link error={this.state.error} onFormSubmit={this.handleFormSubmit} startLoading={function(e) {this.setState({loading: e, error: !e})}.bind(this)} />, text: "По ссылке"}};
    let content;
    if (this.state.loading) {
      content = <Loading />
    } else if (this.state.result) {
      content = <Result back={function() {this.setState({result: false, error: false})}.bind(this)} data={this.state.data.data} />;
    } else {
      content = tabs[this.state.tab].component;
    }
    return (
      <div className={styles.app}>
        <MenuBar tabs={tabs} tab={this.state.tab} result={this.state.result} onChangeTab={this.changeTab} />
        <Content>{content}</Content>
      </div>
    );
  },
});

var MenuBar = React.createClass({
  onChangeTab(e) {
    this.props.onChangeTab(e.target.id);
  },
  render: function() {
    let tabname = this.props.tab;
    let f = this.onChangeTab;
    let menuItems = [];
    for (tab in this.props.tabs) {
      let classes = styles.menuButton;
      if (!this.props.result && tab == tabname) {
        classes += ' ' + styles.menuButtonActive;
      }
      menuItems.push(<a className={classes} id={tab}
        key={tab} onClick={f}>{this.props.tabs[tab].text}</a>);
    }
    return (
      <div className={styles.menuBar}>
        {menuItems}
      </div>
    );
  }
});

var Content = React.createClass({
  render: function() {
    return (
      <div className={styles.content}>
        {this.props.children}
      </div>
    );
  }
});

ReactDOM.render(
  <App />,
  document.getElementById('app')
);
