# Aurguide

Aurguide is a comprehensive platform designed to assist students in navigating the complexities of studying abroad. By leveraging modern technologies, Aurguide streamlines the process of university selection, application submissions, visa appointments, and job placements.

## Features

- **University Recommendations:** Personalized suggestions based on academic achievements, budget, and preferences.
- **Application Assistance:** Automated form filling and document management for university applications.
- **Visa Appointment Scheduling:** Integration to facilitate booking visa appointments.
- **Job Placement Support:** Guidance and resources for securing employment opportunities abroad.

## Technologies Used

- **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Frontend Framework:** [React](https://reactjs.org/)
- **Retrieval-Augmented Generation (RAG):** Combining retrieval-based and generative AI models to provide accurate and context-aware information.
- **Web Scraping:** Collecting up-to-date information from university websites and official portals to ensure accurate recommendations.

## Getting Started

### Prerequisites

- **Python 3.8+**
- **Node.js 14+**
- **npm 6+**

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/aurguide.git
   cd aurguide
   ```

2. **Backend Setup:**

   - Navigate to the backend directory:

     ```bash
     cd backend
     ```

   - Create a virtual environment and activate it:

     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```

   - Install the required dependencies:

     ```bash
     pip install -r requirements.txt
     ```

   - Start the FastAPI server:

     ```bash
     uvicorn main:app --reload
     ```

3. **Frontend Setup:**

   - Navigate to the frontend directory:

     ```bash
     cd ../frontend
     ```

   - Install the required dependencies:

     ```bash
     npm install
     ```

   - Start the React development server:

     ```bash
     npm start
     ```

## Contributing

We welcome contributions from the community. Please refer to our [contribution guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

We extend our gratitude to the developers and contributors of FastAPI, React, and the open-source community for their invaluable tools and resources.

---

*Note: This README provides a high-level overview of the Aurguide project. For detailed documentation, please refer to the [docs](docs/) directory.*
