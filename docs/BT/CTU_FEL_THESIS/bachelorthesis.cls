\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{bachelorthesis}[2025/10/02 v4.2 (Bachelor variant, LuaLaTeX-ready)]

\RequirePackage{iftex}

\newif\if@literature \@literaturefalse
\DeclareOption{literature}{\@literaturetrue}

\newif\if@statement \@statementfalse
\DeclareOption{statement}{\@statementtrue}

\newif\if@print \@printfalse
\DeclareOption{print}{\@printtrue}

\newif\if@bibtexbackend \@bibtexbackendfalse
\DeclareOption{bibtex}{\@bibtexbackendtrue}
\DeclareOption{biber}{\@bibtexbackendfalse}

\ProcessOptions\relax

% Page layout depends on whether this is a statement or the full thesis
\if@statement
  \LoadClass[twoside,a4paper,11pt]{article}
  \RequirePackage[margin=2cm, bottom=2.5cm, top=2cm, right=2cm]{geometry}

  % Delimiter between front and main matter
  \newcommand{\mainmatter}{
    \newpage
    \pagenumbering{arabic}
  }
\else
  % For on-screen drafts, a constant left/right margin is often preferred.
  % Use `\documentclass[print]{bachelorthesis}` for final double-sided printing.
  \if@print
    \LoadClass[11pt,twoside,a4paper]{book}
    % Inner margin for binding, slightly smaller outer margin.
    \RequirePackage[inner=3cm,outer=2cm,top=3cm,bottom=2cm]{geometry}
  \else
    \LoadClass[11pt,oneside,a4paper]{book}
    % Constant margins for PDF reading.
    \RequirePackage[margin=2cm,left=3cm,top=3cm,bottom=2cm]{geometry}
  \fi
\fi

\RequirePackage{graphicx}
\RequirePackage{tabularx}

% LuaLaTeX/XeLaTeX: native UTF-8 + font handling
\ifPDFTeX
  % pdfTeX users should load inputenc/fontenc in the document preamble if needed.
\else
  \RequirePackage{fontspec}
  \defaultfontfeatures{Ligatures=TeX}
\fi

\RequirePackage{microtype}

% Institution defaults
\newcommand\University{Czech Technical University in Prague}
\newcommand\Faculty{Faculty of Electrical Engineering}
\newcommand\Department{Department of Microelectronics}

% Thesis metadata (defaults can be overridden in the document)
\newcommand\ThesisType{Thesis}
\newcommand\StudyProgram{Electrical Engineering and Computer Science}
\newcommand\StudyBranch{Electrical Engineering and Computer Science}

% Used on statement pages
\newcommand\Address{Technick{\'a}~2, 160 00 Prague 6, Czech Republic}

% User overrides
\newcommand{\university}[1]{\renewcommand\University{#1}}
\newcommand{\faculty}[1]{\renewcommand\Faculty{#1}}
\newcommand{\department}[1]{\renewcommand\Department{#1}}
\newcommand{\thesistype}[1]{\renewcommand\ThesisType{#1}}
\newcommand{\studyprogram}[1]{\renewcommand\StudyProgram{#1}}
\newcommand{\studybranch}[1]{\renewcommand\StudyBranch{#1}}

% Supervisor/affiliation metadata
\def \@supervisor{Unknown}
\newcommand{\supervisor}[1]{\def\@supervisor{#1}}

\def \@authorAffiliation{Unknown}
\newcommand{\authorAffiliation}[1]{\def\@authorAffiliation{#1}}

\def \@supervisorAffiliation{Unknown}
\newcommand{\supervisorAffiliation}[1]{\def\@supervisorAffiliation{#1}}

% Default value; usually overridden in the main document.
\def \@placeyear{Prague 2026}
\newcommand{\placeyear}[1]{\def\@placeyear{#1}}

% Convenience references
\newcommand{\figref}[1]{\figurename~\ref{#1}}
\newcommand{\tabref}[1]{Table~\ref{#1}}
\newcommand{\secref}[1]{Section~\ref{#1}}

% Title pages
\renewcommand\maketitle{\par
  % Pick the appropriate title page variant
  \if@literature
    \@literaturetitle
  \else
    \if@statement
      \@statementtitle
    \else
      \@fullthesis
    \fi
  \fi

  \global\let\thanks\relax
  \global\let\maketitle\relax
  \global\let\@maketitle\relax
  \global\let\@thanks\@empty
  \global\let\@author\@empty
  \global\let\@date\@empty
  \global\let\@title\@empty
  \global\let\title\relax
  \global\let\author\relax
  \global\let\date\relax
  \global\let\and\relax
}

% Title page: full thesis
\def\@fullthesis{%
  \frontmatter
  \begin{center}
    {\LARGE\bfseries
    \University}\\[3mm]
    {\Large\sffamily
    \Faculty}\\[2mm]
    {\large\sffamily
    \Department}\\[15mm]
    \IfFileExists{images/LogoCVUT.pdf}{\includegraphics[width=60mm]{images/LogoCVUT}}{}
    \vspace{20mm}
    
    {\LARGE\bfseries\@title}\\[8mm]
    {\Large\sffamily \ThesisType}\\[10mm]
    {\Large\emph{\@author}}\\[45mm]
    {\large
      Study program: \StudyProgram\\[3mm]
      Supervisor: \@supervisor\\
    }
    \vfill
    \@placeyear\\
  \end{center}
  \thispagestyle{empty}

  % Page 2
  \newpage
  \rule{0pt}{0pt}
  \vfill
  \begin{description}
    \item[Thesis Supervisor:] ~\\
    \@supervisor\\
    \@supervisorAffiliation
  \end{description}
  Copyright {\copyright} {\@date} {\@author}

  % Declaration removed - use separate declaration.tex file with CTU-required wording
}

% Title page: statement
\def\@statementtitle{%
  \pagenumbering{Roman}
  \begin{center}
    {\LARGE\sffamily
      \University\\
      \Faculty\\
      \Department\\
      \vspace{50mm}
      \IfFileExists{images/LogoCVUT.pdf}{\includegraphics[width=130mm]{images/LogoCVUT}}{}
      \vfill
      {\LARGE\bfseries \MakeUppercase{\ThesisType} STATEMENT}
    }
  \end{center}
  \thispagestyle{empty}

  % Page 2
  \newpage
  \if@print
    ~\thispagestyle{empty}
    \newpage
  \fi

  \begin{center}
    {\Large\sffamily
      \University\\
      \Faculty\\
      \Department
      \vfill

      {\sffamily\bfseries\@title}\\
      \bigskip
      by\\
      \bigskip
      {\large\emph{\@author}}\\
      \vfill

      {\large
        Study program: \StudyProgram\\
        Field of study: \StudyBranch
      }\\

      \vspace{1cm}
      Thesis statement document
      \vspace{1cm}
      \@placeyear
    }
  \end{center}
  \thispagestyle{empty}

  \frontmatter
  \newpage

  % Page 3 - author and supervisor
  \pagenumbering{roman}

  {\small
    \noindent The thesis was written at the \Department, \Faculty of the Czech Technical University in Prague.

    \vspace{.5cm}
    \noindent\hbox to 3cm{\hbox{Author:}\hss}\parbox[t]{8cm}{
      \textbf{\@author}\\
      \@authorAffiliation}

    \vspace{.5cm}
    \noindent\hbox to 3cm{\hbox{Supervisor:}\hss}\parbox[t]{8cm}{%
      \textbf{\@supervisor}\\
      \@supervisorAffiliation}

    \vspace{1cm}
    \noindent\hbox to 3cm{\hbox{Reviewers:}\hss}\parbox[t]{8cm}{%
      \vrule width 5cm height 0pt depth 0.5pt\\[.5cm]
      \vrule width 5cm height 0pt depth 0.5pt\\[.5cm]
      \vrule width 5cm height 0pt depth 0.5pt
    }

    \bigskip\bigskip
    \noindent This thesis statement was distributed on ................

    \bigskip
    \noindent The defence of the thesis will be held on ............................ at .......................... in the meeting room No. ............... .

    \bigskip
    \noindent Those interested may get acquainted with the thesis at the Dean Office of the Faculty of Electrical Engineering of the CTU in Prague, at the Department for Science and Research, \Address.

    \vfill
    \begin{center}
      \bigskip\bigskip
      ............................................................................\\
      \medskip
      Chairman of the Board for the Defence of the Thesis\\
      \Department\\
      \Faculty\\
      \University\\
      \Address
    \end{center}
  }
  \newpage
}

\def\@literaturetitle{%
  \begin{center}
    {\Large\sffamily
      \University\\
      \Faculty\\
      \Department\\
      \vspace{30mm}
      \IfFileExists{images/LogoCVUT.pdf}{\includegraphics[width=50mm]{images/LogoCVUT}}{}
      \vspace{20mm}
      {\Large\bfseries LIST OF PERSONAL PUBLICATIONS}
      \vspace{30mm}
      \textit{\@author}
      \vspace{10mm}
      \@placeyear
      \vfill
      {\footnotesize Automatically generated list}
    }
  \end{center}
  \thispagestyle{empty}

  % Page 2
  \newpage
  \pagenumbering{arabic}
}

% Biblatex (fullcite helper)
\if@bibtexbackend
  \RequirePackage[style=ieee,backend=bibtex]{biblatex}
\else
  \RequirePackage[style=ieee,backend=biber]{biblatex}
\fi
\DeclareBibliographyCategory{fullcited}
\newcommand{\bibentry}[1]{\fullcite{#1}\addtocategory{fullcited}{#1}}

\RequirePackage[nottoc]{tocbibind}
\RequirePackage{setspace}

% Hyperlinks: keep link styling subtle
\RequirePackage{xcolor}
\RequirePackage{hyperref}
\hypersetup{colorlinks=true,citecolor=black,linkcolor=black,urlcolor=black}

% PDF metadata
\makeatletter
\AtBeginDocument{%
  \hypersetup{%
    pdftitle={\@title},
    pdfauthor={\@author},
    pdfsubject={\ThesisType},
  }%
}
\makeatother
