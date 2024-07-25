import React, { useEffect, useState } from 'react';
import './style.css';
import { getTextStyle, getDataTypeClass } from './utilities/styleHelpers';

const Dashboard = () => {
  const [traffic, setTraffic] = useState([]);
  const [subscriptions, setSubscriptions] = useState([]);
  const [loadTraffic, setLoadTraffic] = useState(false);
  const [loadSubscriptions, setLoadSubscriptions] = useState(false);

  // Fetch Traffic Data
  useEffect(() => {
    if (loadTraffic) {
      const fetchTrafficData = async () => {
        try {
          const response = await fetch('http://localhost:5001/api/utm-codes');
          if (!response.ok) throw new Error(`HTTP status ${response.status}`);
          const data = await response.json();
          setTraffic(data);
        } catch (error) {
          console.error('Failed to fetch traffic data:', error);
        }
      };
      fetchTrafficData();
    } else {
      setTraffic([]); // Optionally clear data when toggle is off
    }
  }, [loadTraffic]);

  // Fetch Subscription Data
  useEffect(() => {
    if (loadSubscriptions) {
      const fetchSubscriptionData = async () => {
        try {
          const response = await fetch('http://localhost:5001/api/stripe-transactions');
          if (!response.ok) throw new Error(`HTTP status ${response.status}`);
          const data = await response.json();
          setSubscriptions(data);
        } catch (error) {
          console.error('Failed to fetch subscription data:', error);
        }
      };
      fetchSubscriptionData();
    } else {
      setSubscriptions([]); // Optionally clear data when toggle is off
    }
  }, [loadSubscriptions]);

  return (
    <div className="frame">
      <div className="div">
        <div className="frame-wrapper">
          <h1 className="text-wrapper">Dashboard</h1>
        </div>
        <div className="div-wrapper">
          <div className="div-3">
            <div className="frame-wrapper-2">
              <div className="div-2">
                <div className="div-wrapper-2">
                  <h2 className="text-wrapper-2">Traffic</h2>
                  <label>
                    Load Traffic
                    <input
                      type="checkbox"
                      checked={loadTraffic}
                      onChange={(e) => setLoadTraffic(e.target.checked)}
                    />
                  </label>
                </div>
                <ul>
                  {traffic.map((trafficItem) => (
                    <li key={trafficItem.id} className="div-wrapper-2">
                      <div className={getDataTypeClass(trafficItem.utm_source)}>{trafficItem.utm_source}</div>
                      <div className={getDataTypeClass(trafficItem.visits)}>{trafficItem.visits}</div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
            <div className="div-2">
              <div className="div-wrapper-2">
                <h2 className="text-wrapper-2">Subscriptions</h2>
                <label>
                  Load Subscriptions
                  <input
                    type="checkbox"
                    checked={loadSubscriptions}
                    onChange={(e) => setLoadSubscriptions(e.target.checked)}
                  />
                </label>
              </div>
              <ul>
                {subscriptions.map((item, index) => (
                  <li key={index} className="div-wrapper-2">
                    <div className={getDataTypeClass(item.date)}>{item.date}</div>
                    <div className={getDataTypeClass(item.amount)}>{item.amount}</div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
