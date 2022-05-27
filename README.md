\begin{appendices}
\chapter{Using the API with Postman}\label{appendix:appendix1}

This quick guide illustrates how to launch the Flask server and make requests to any of the explanation methods in the API using Postman. The code, requirements, Dockerfile, and example use cases are available in the project's repository.

\section{Launching the Server}

\subsection{Using Python}

\begin{enumerate}
    \item Clone the repository.
    \item From the root folder, create a virtual environment for the installation of the required libraries with:
            \begin{verbatim}
                python -m venv .
            \end{verbatim}
    
    \item Use pip to install the dependencies from the requirements file.
            \begin{verbatim}
                pip -r requirements.txt
            \end{verbatim}
    \item Once all the dependencies have been installed, access the XAI API folder and execute the script with:
            \begin{verbatim}
                python app.py
            \end{verbatim}
    
\end{enumerate}


\subsection{Using Docker}

\begin{enumerate}
    \item Clone the repository.
    \item From the XAI API folder, execute the following command to build a Docker Image:
            \begin{verbatim}
                docker build -t <tag_name> .
            \end{verbatim}
        The associated tag name you choose will be used to refer to the docker image that will be generated.
    \item Run the container to launch the server. The -p option maps the port from the container to the real system, to allow making requests to the server.
            \begin{verbatim}
                docker run -p 5000:5000 <tag_name>
            \end{verbatim}
    
\end{enumerate}

\section{Making Requests}

If the server was launched correctly, a similar message to the one in the image should appear, meaning that it is ready to receive requests to the specified address and port.

\begin{figure}[H]
\includegraphics[width=\textwidth]{img/ServerLaunched.PNG}
\end{figure}

\begin{enumerate}
    \item To make requests, open Postman and go to \textit{My Workspace $>$ File $>$ New Tab}.
    \item To get information about how to use a specific method, we can make a GET request. In the URL bar, specify the address and port of the server, followed by the name of the method, and send the request. The response is displayed in the bottom part of the console. For example, for Tabular/Importance:
    
    \begin{figure}[H]
\includegraphics[width=\textwidth]{img/GetPostman.PNG}
\end{figure}
    
    \item To execute the methods, we have to make a POST request. To do so, change the request type to POST and go to \textit{Body $>$ form-data}. Here is were we specify required parameters, such as the \textit{model} and \textit{data} files, and the \textit{params} object. In this example, I am using the cancer use case model and data. The only parameters included in the \textit{params} object were the \textit{backend} (sklearn) and the \textit{model\_task} (classification).
    
        \begin{figure}[H]
\includegraphics[width=\textwidth]{img/PostPostman.PNG}
\end{figure}
    
\end{enumerate}

\subsection{Visualizing Explanations}

The responses to the HTTP requests are given in JSON format. However, most of the methods return responses that also contain the URLs to plots or graphs of the explanations in HTML or PNG format. Before accessing the explanations, it is necessary to change the default JSON mime-type.

\begin{enumerate}
    \item To visualize these explanations, click on the URL in the response. It will open a new request tab with the specified URL.
    \item Go to \textit{Headers} and disable the \textit{Accept} attribute.
    \item Add a new header with the same name, \textit{Accept}, as key and specify the value according to the type of file you are trying to access. For .png files, specify \textit{image/png}. For .html files, specify \textit{text/html}. Finally, send the request.
    
            \begin{figure}[H]
\includegraphics[width=\textwidth]{img/ViewerPostman.PNG}
\end{figure}
    
    
    
    
    
\end{enumerate}



\end{appendices}
