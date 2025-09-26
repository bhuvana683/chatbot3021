/* frontend/src/pages/Projects/Projects.tsx */

import { useEffect, useState } from "react";
import API from "../../services/api";
import { useNavigate } from "react-router-dom";
import "./Projects.css"; // Import the CSS

type Project = {
  id: string;
  name: string;
};

export default function Projects() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const token = localStorage.getItem("token");
        const res = await API.get("/projects", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setProjects(res.data);
      } catch (err) {
        console.error(err);
        alert("Error fetching projects");
      } finally {
        setLoading(false);
      }
    };
    fetchProjects();
  }, []);

  const handleSelectProject = (id: string) => {
    localStorage.setItem("selectedProjectId", id);
    navigate("/chat");
  };

  if (loading) {
    return <p>Loading projects...</p>;
  }

  return (
    <div className="projects-container">
      <h2>Your Projects</h2>
      {projects.length === 0 ? (
        <p>No projects found.</p>
      ) : (
        <ul className="projects-list">
          {projects.map((p) => (
            <li
              key={p.id}
              className="project-item"
              onClick={() => handleSelectProject(p.id)}
            >
              {p.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
