'use client'
import React, { useState, useEffect } from 'react';
import styles from './page.module.css';

export default function Home() {
  const [rankings, setRankings] = useState([]);

  useEffect(() => {
    fetch('/mock_rankings.json')
    .then((response) => response.json())
    .then((data) => setRankings(data))
    .catch((error) => console.error("Error fetching data: ", error));
  }, []);

  return (
    <main className={styles.main}>
      <h1 className={styles.title}>Welcome to Sam and Jasmine's League Ranker!</h1>
      <p className={styles.description}>2023 LoL Worlds Ranking System Developed by Sam and Jasmine</p>

      <h2 className={styles.subtitle}>Rankings</h2>
      <u1 className={styles.list}>
        {rankings.map((team, index) => (
          <li key={index} className={styles.listItem}>
            <strong> Rank {team.rank}:</strong> {team.team_name}
          </li>
        ))}
      </u1>
    </main>
  );
}
