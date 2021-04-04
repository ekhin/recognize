import React, { Component } from 'react';
// import CaloriesInfo from './CaloriesInfo';
import Userlogin from './Userlogin';
import FoodInfo from './FoodInfo';
import Uploads from './Uploads';
import Cookies from 'universal-cookie';

import { Navbar } from 'rsuite';



export default class Main extends React.Component {


  render() {
    return (
      <div>
        <Navbar bg="dark">
          <Navbar.Header>
            
          </Navbar.Header>
        </Navbar>
        <h1> Estimate My Daily Intake! </h1>
        <Uploads/>
      </div>
    )
  }
}
