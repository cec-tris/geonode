/*
#########################################################################
#
# Copyright (C) 2019 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################
*/

import React from 'react';
import PropTypes from 'prop-types';
import CircularProgress from 'material-ui/CircularProgress';
import HoverPaper from '../../atoms/hover-paper';
import styles from './styles';


class StorageUsage extends React.Component {
  static propTypes = {
    storage: PropTypes.number,
  }

  static contextTypes = {
    muiTheme: PropTypes.object.isRequired,
  }

  render() {
    let storage = this.props.storage;
    if (storage === undefined) {
      storage = 'N/A';
    } else if (typeof storage === 'number') {
      if (storage < 0) {
        storage = <CircularProgress size={this.context.muiTheme.spinner.size} />;
      } else {
        let mbMem = (storage / 1024 / 1024);
        let mbMemFormated;
        if (mbMem < 1024) {
          mbMemFormated = mbMem.toFixed(0);
          storage = `${mbMemFormated} MB`;
        } else {
          mbMem = mbMem /1024
          mbMemFormated = Math.floor(mbMem);
          storage = `${mbMemFormated} GB`;
        }
      }
    }
    return (
      <HoverPaper style={styles.content}>
        <h5>Storage Usage</h5>
        <div style={styles.stat}>
          <h3>{storage}</h3>
        </div>
      </HoverPaper>
    );
  }
}


export default StorageUsage;
