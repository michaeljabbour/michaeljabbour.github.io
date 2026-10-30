# TikZ Patterns for Scientific Diagrams

Complete pattern library for creating publication-ready diagrams using TikZ and PGFPlots.

**Philosophy:** TikZ provides precise, vectorized diagrams that integrate seamlessly with LaTeX. This guide provides reusable patterns for common scientific visualizations.

---

## Table of Contents

1. [TikZ Basics](#tikz-basics)
2. [Essential Libraries](#essential-libraries)
3. [Neural Network Diagrams](#neural-network-diagrams)
4. [Attention Mechanisms](#attention-mechanisms)
5. [Flowcharts and Algorithms](#flowcharts-and-algorithms)
6. [Graph Theory Diagrams](#graph-theory-diagrams)
7. [Mathematical Plots (PGFPlots)](#mathematical-plots-pgfplots)
8. [Coordinate Systems](#coordinate-systems)
9. [LaTeX Integration](#latex-integration)
10. [Complete Pattern Examples](#complete-pattern-examples)

---

## TikZ Basics

### Minimal TikZ Document

```latex
\documentclass{article}
\usepackage{tikz}

\begin{document}
\begin{tikzpicture}
  % Your diagram here
  \draw (0,0) -- (2,1);
  \node at (1,0.5) {Hello TikZ};
\end{tikzpicture}
\end{document}
```

### Core Concepts

```latex
% Coordinates
\coordinate (A) at (0,0);
\coordinate (B) at (2,1);

% Paths
\draw (A) -- (B);              % Line
\draw (A) rectangle (B);       % Rectangle
\draw (A) circle (1cm);        % Circle
\draw (A) ellipse (2cm and 1cm); % Ellipse

% Nodes (text boxes)
\node at (1,1) {Text};
\node[circle,draw] at (2,2) {Circle node};
\node[rectangle,draw,fill=blue!20] at (3,3) {Box};

% Styling
\draw[thick,red,dashed] (0,0) -- (1,1);
\draw[->] (0,0) -- (1,0);      % Arrow
\draw[-latex] (0,0) -- (0,1);  % LaTeX arrow style
```

### Node Positioning

```latex
% Relative positioning (requires positioning library)
\node (A) at (0,0) {A};
\node (B) [right=of A] {B};
\node (C) [below=of A] {C};
\node (D) [above right=of A] {D};

% Manual offset
\node (E) at ($(A) + (2,1)$) {E};  % Requires calc library
```

---

## Essential Libraries

### Common Libraries Setup

```latex
\usepackage{tikz}
\usetikzlibrary{
  positioning,    % Advanced node positioning
  shapes,         % Geometric shapes
  arrows.meta,    % Modern arrow styles
  decorations,    % Path decorations
  calc,           % Coordinate calculations
  fit,            % Fitting boxes around nodes
  backgrounds,    % Background layers
  patterns,       % Fill patterns
  shadows,        % Drop shadows
  matrix,         % Matrix layouts
}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
```

### Library-Specific Features

```latex
% positioning: Better node placement
\node[right=2cm of A] {B};

% shapes: Custom node shapes
\node[ellipse,draw] {Ellipse};
\node[diamond,draw] {Diamond};
\node[trapezium,draw] {Trap};

% arrows.meta: Modern arrows
\draw[-Stealth] (0,0) -- (1,0);
\draw[-Latex] (0,0) -- (0,1);
\draw[<->] (0,0) -- (1,1);

% calc: Coordinate math
\coordinate (mid) at ($(A)!0.5!(B)$);

% fit: Bounding boxes
\node[fit={(A) (B) (C)}, draw, dashed] {};
```

---

## Neural Network Diagrams

### Pattern 1: Simple Feed-Forward Network

```latex
\begin{tikzpicture}[
  neuron/.style={circle,draw,minimum size=0.8cm,inner sep=0pt},
  layer/.style={rectangle,draw,minimum width=1.5cm,minimum height=3cm},
  arrow/.style={-Stealth,thick}
]

% Input layer
\foreach \y in {1,2,3} {
  \node[neuron,fill=blue!20] (I\y) at (0,\y) {};
}
\node[above=0.2cm of I3] {Input};

% Hidden layer
\foreach \y in {1,2,3,4} {
  \node[neuron,fill=green!20] (H\y) at (3,\y-0.5) {};
}
\node[above=0.2cm of H4] {Hidden};

% Output layer
\foreach \y in {1,2} {
  \node[neuron,fill=red!20] (O\y) at (6,\y+0.5) {};
}
\node[above=0.2cm of O2] {Output};

% Connections
\foreach \i in {1,2,3} {
  \foreach \j in {1,2,3,4} {
    \draw[arrow,gray!50] (I\i) -- (H\j);
  }
}
\foreach \i in {1,2,3,4} {
  \foreach \j in {1,2} {
    \draw[arrow,gray!50] (H\i) -- (O\j);
  }
}

% Layer labels
\node[below=0.5cm of I1] {$x_1, x_2, x_3$};
\node[below=0.5cm of O1] {$y_1, y_2$};

\end{tikzpicture}
```

### Pattern 2: Convolutional Layer

```latex
\begin{tikzpicture}[
  cube/.style={draw,minimum width=1cm,minimum height=1cm,fill=blue!20},
  operation/.style={rectangle,draw,rounded corners,fill=yellow!20}
]

% Input volume (32x32x3)
\foreach \z in {0,0.2,0.4} {
  \draw[fill=blue!20,opacity=0.7]
    (\z,\z) rectangle ++(2,2);
}
\node[below] at (1,0) {$32 \times 32 \times 3$};

% Conv operation
\node[operation] at (3.5,1) {Conv\\$5\times5\times64$};

% Feature maps (28x28x64)
\foreach \z in {0,0.1,0.2,...,1} {
  \draw[fill=green!20,opacity=0.5]
    (5+\z,\z) rectangle ++(1.5,1.5);
}
\node[below] at (6,0) {$28 \times 28 \times 64$};

% Pooling
\node[operation] at (8.5,1) {MaxPool\\$2\times2$};

% Pooled output (14x14x64)
\foreach \z in {0,0.1,0.2,...,1} {
  \draw[fill=red!20,opacity=0.5]
    (10+\z,0.5+\z) rectangle ++(1,1);
}
\node[below] at (11,0) {$14 \times 14 \times 64$};

% Arrows
\draw[-Stealth,thick] (2.2,1) -- (2.8,1);
\draw[-Stealth,thick] (4.2,1) -- (4.8,1);
\draw[-Stealth,thick] (7.2,1) -- (7.8,1);

\end{tikzpicture}
```

### Pattern 3: Residual Block

```latex
\begin{tikzpicture}[
  block/.style={rectangle,draw,minimum width=2cm,minimum height=0.8cm,fill=blue!20},
  operation/.style={rectangle,draw,rounded corners,fill=yellow!20,minimum width=1.5cm}
]

% Main path
\node[block] (input) at (0,0) {Input};
\node[operation] (conv1) at (0,-1.5) {Conv $3\times3$};
\node[operation] (relu1) at (0,-2.5) {ReLU};
\node[operation] (conv2) at (0,-3.5) {Conv $3\times3$};

% Skip connection
\draw[-Stealth,thick,red] (input.east) -- ++(1,0) |- (conv2.east);
\node[right,red] at (1,-1.5) {skip};

% Addition
\node[circle,draw,minimum size=0.8cm] (add) at (0,-4.5) {$+$};
\draw[-Stealth,thick] (input) -- (conv1);
\draw[-Stealth,thick] (conv1) -- (relu1);
\draw[-Stealth,thick] (relu1) -- (conv2);
\draw[-Stealth,thick] (conv2) -- (add);

% Output
\node[operation] (relu2) at (0,-5.5) {ReLU};
\node[block] (output) at (0,-6.5) {Output};
\draw[-Stealth,thick] (add) -- (relu2);
\draw[-Stealth,thick] (relu2) -- (output);

\end{tikzpicture}
```

### Pattern 4: Transformer Encoder Block

```latex
\begin{tikzpicture}[
  block/.style={rectangle,draw,minimum width=2.5cm,minimum height=0.7cm,fill=blue!10},
  mha/.style={rectangle,draw,minimum width=2.5cm,minimum height=1cm,fill=orange!20},
  ffn/.style={rectangle,draw,minimum width=2.5cm,minimum height=1cm,fill=green!20}
]

% Input
\node[block] (input) at (0,0) {Input Embeddings};

% Multi-head attention
\node[mha] (mha) at (0,-1.5) {Multi-Head\\Attention};

% Add & Norm 1
\node[block] (norm1) at (0,-2.8) {Add \& Norm};

% Skip connection 1
\draw[-Stealth,thick,red,dashed] (input.east) -- ++(0.7,0) |- (norm1.east);

% Feed-forward
\node[ffn] (ffn) at (0,-4.2) {Feed-Forward\\Network};

% Add & Norm 2
\node[block] (norm2) at (0,-5.5) {Add \& Norm};

% Skip connection 2
\draw[-Stealth,thick,red,dashed] (norm1.east) -- ++(0.7,0) |- (norm2.east);

% Output
\node[block] (output) at (0,-6.5) {Output};

% Main path arrows
\draw[-Stealth,thick] (input) -- (mha);
\draw[-Stealth,thick] (mha) -- (norm1);
\draw[-Stealth,thick] (norm1) -- (ffn);
\draw[-Stealth,thick] (ffn) -- (norm2);
\draw[-Stealth,thick] (norm2) -- (output);

% Labels
\node[left=0.3cm of input] {$x$};
\node[left=0.3cm of output] {$z$};

\end{tikzpicture}
```

---

## Attention Mechanisms

### Pattern 5: Self-Attention Visualization

```latex
\begin{tikzpicture}[
  word/.style={rectangle,draw,minimum width=1cm,minimum height=0.6cm,fill=blue!10},
  qkv/.style={rectangle,draw,rounded corners,fill=green!20,minimum width=0.8cm}
]

% Input words
\foreach \i/\w in {0/The,1/cat,2/sat} {
  \node[word] (w\i) at (\i*1.5,0) {\w};
}

% Q, K, V projections
\foreach \i in {0,1,2} {
  \node[qkv] (q\i) at (\i*1.5,-1.5) {Q};
  \node[qkv] (k\i) at (\i*1.5,-2.5) {K};
  \node[qkv] (v\i) at (\i*1.5,-3.5) {V};

  \draw[-Stealth] (w\i) -- (q\i);
  \draw[-Stealth] (w\i) -- (k\i);
  \draw[-Stealth] (w\i) -- (v\i);
}

% Attention mechanism
\node[rectangle,draw,fill=yellow!20,minimum width=4cm,minimum height=1cm]
  (attn) at (1.5,-5) {Attention($Q$, $K$, $V$)};

\foreach \i in {0,1,2} {
  \draw[-Stealth] (q\i) -- (attn);
  \draw[-Stealth] (k\i) -- (attn);
  \draw[-Stealth] (v\i) -- (attn);
}

% Output
\foreach \i/\w in {0/The,1/cat,2/sat} {
  \node[word,fill=red!10] (o\i) at (\i*1.5,-6.5) {\w'};
  \draw[-Stealth] (attn) -- (o\i);
}

\end{tikzpicture}
```

### Pattern 6: Multi-Head Attention

```latex
\begin{tikzpicture}[
  head/.style={rectangle,draw,rounded corners,fill=blue!20,minimum width=1.2cm,minimum height=2cm}
]

% Input
\node[rectangle,draw,minimum width=5cm,minimum height=0.8cm,fill=green!10]
  (input) at (2.5,0) {Input: $d_{\text{model}} = 512$};

% Multiple heads
\foreach \i in {0,1,2,3} {
  \node[head] (h\i) at (\i*1.5,-2) {Head \i};
  \draw[-Stealth] (input) -- (h\i);
  \node[below,font=\scriptsize] at (h\i.south) {$d_k=64$};
}

% Concatenation
\node[rectangle,draw,fill=yellow!20,minimum width=5cm,minimum height=0.8cm]
  (concat) at (2.5,-4) {Concatenate};

\foreach \i in {0,1,2,3} {
  \draw[-Stealth] (h\i) -- (concat);
}

% Linear projection
\node[rectangle,draw,fill=orange!20,minimum width=5cm,minimum height=0.8cm]
  (linear) at (2.5,-5.5) {Linear: $W^O$};

\draw[-Stealth] (concat) -- (linear);

% Output
\node[rectangle,draw,minimum width=5cm,minimum height=0.8cm,fill=red!10]
  (output) at (2.5,-7) {Output: $d_{\text{model}} = 512$};

\draw[-Stealth] (linear) -- (output);

\end{tikzpicture}
```

---

## Flowcharts and Algorithms

### Pattern 7: Algorithm Flowchart

```latex
\begin{tikzpicture}[
  start/.style={ellipse,draw,fill=green!20,minimum width=2cm},
  process/.style={rectangle,draw,fill=blue!20,minimum width=2.5cm,minimum height=1cm},
  decision/.style={diamond,draw,fill=yellow!20,aspect=2,text width=1.5cm,align=center},
  end/.style={ellipse,draw,fill=red!20,minimum width=2cm}
]

% Start
\node[start] (start) at (0,0) {Start};

% Initialize
\node[process] (init) at (0,-1.5) {Initialize\\$x = 0$};

% Loop condition
\node[decision] (cond) at (0,-3.5) {$x < N$?};

% Process
\node[process] (proc) at (0,-5.5) {Process $x$\\$x = x + 1$};

% End
\node[end] (end) at (3,-3.5) {End};

% Arrows
\draw[-Stealth,thick] (start) -- (init);
\draw[-Stealth,thick] (init) -- (cond);
\draw[-Stealth,thick] (cond) -- node[right] {Yes} (proc);
\draw[-Stealth,thick] (proc) -- ++(-2,0) |- (cond);
\draw[-Stealth,thick] (cond) -- node[above] {No} (end);

\end{tikzpicture}
```

### Pattern 8: Training Pipeline

```latex
\begin{tikzpicture}[
  box/.style={rectangle,draw,rounded corners,fill=blue!10,minimum width=2cm,minimum height=0.8cm},
  data/.style={cylinder,draw,fill=green!20,shape border rotate=90,minimum width=1.5cm,minimum height=1cm}
]

% Data
\node[data] (data) at (0,0) {Dataset};

% Preprocessing
\node[box] (prep) at (3,0) {Preprocess};

% Training
\node[box] (train) at (6,0) {Train Model};

% Validation
\node[box] (val) at (6,-2) {Validate};

% Decision
\node[diamond,draw,fill=yellow!20,aspect=2] (dec) at (3,-2) {Good?};

% Save
\node[box,fill=green!20] (save) at (0,-2) {Save Model};

% Arrows
\draw[-Stealth,thick] (data) -- (prep);
\draw[-Stealth,thick] (prep) -- (train);
\draw[-Stealth,thick] (train) -- (val);
\draw[-Stealth,thick] (val) -- (dec);
\draw[-Stealth,thick] (dec) -- node[above] {Yes} (save);
\draw[-Stealth,thick] (dec) -- node[right] {No} ++(0,1) -| (train);

\end{tikzpicture}
```

---

## Graph Theory Diagrams

### Pattern 9: Directed Graph

```latex
\begin{tikzpicture}[
  vertex/.style={circle,draw,fill=blue!20,minimum size=0.8cm},
  edge/.style={-Stealth,thick}
]

% Vertices
\node[vertex] (v1) at (0,0) {1};
\node[vertex] (v2) at (2,1) {2};
\node[vertex] (v3) at (2,-1) {3};
\node[vertex] (v4) at (4,0) {4};

% Edges with weights
\draw[edge] (v1) -- node[above] {5} (v2);
\draw[edge] (v1) -- node[below] {3} (v3);
\draw[edge] (v2) -- node[above] {2} (v4);
\draw[edge] (v3) -- node[below] {4} (v4);
\draw[edge] (v2) to[bend left] node[right] {1} (v3);

\end{tikzpicture}
```

### Pattern 10: Knowledge Graph

```latex
\begin{tikzpicture}[
  entity/.style={rectangle,draw,rounded corners,fill=blue!20,minimum width=1.5cm},
  relation/.style={-Stealth,thick,above,sloped}
]

% Entities
\node[entity] (cat) at (0,0) {Cat};
\node[entity] (animal) at (3,1) {Animal};
\node[entity] (pet) at (3,-1) {Pet};
\node[entity] (mammal) at (6,0) {Mammal};

% Relations
\draw[relation] (cat) -- node {is-a} (animal);
\draw[relation] (cat) -- node {is-a} (pet);
\draw[relation] (animal) -- node {subclass} (mammal);
\draw[relation] (pet) -- node {type-of} (mammal);

\end{tikzpicture}
```

---

## Mathematical Plots (PGFPlots)

### Pattern 11: Function Plot

```latex
\begin{tikzpicture}
\begin{axis}[
  xlabel=$x$,
  ylabel=$f(x)$,
  domain=-2:2,
  samples=100,
  grid=major,
  legend pos=north west,
  width=8cm,
  height=6cm
]

% Plot functions
\addplot[blue,thick] {x^2};
\addplot[red,thick] {exp(x)};
\addplot[green,thick,dashed] {sin(deg(x))};

\legend{$x^2$, $e^x$, $\sin(x)$}

\end{axis}
\end{tikzpicture}
```

### Pattern 12: Scatter Plot with Error Bars

```latex
\begin{tikzpicture}
\begin{axis}[
  xlabel=Epochs,
  ylabel=Accuracy (\%),
  grid=major,
  legend pos=south east,
  width=8cm,
  height=6cm
]

\addplot[
  blue,
  only marks,
  mark=*,
  error bars/.cd,
  y dir=both,
  y explicit
] coordinates {
  (10,75) +- (0,2)
  (20,82) +- (0,1.5)
  (30,87) +- (0,1.2)
  (40,91) +- (0,0.8)
};

\addlegendentry{Model A}

\addplot[
  red,
  only marks,
  mark=square*,
  error bars/.cd,
  y dir=both,
  y explicit
] coordinates {
  (10,72) +- (0,2.5)
  (20,80) +- (0,1.8)
  (30,85) +- (0,1.5)
  (40,89) +- (0,1.0)
};

\addlegendentry{Model B}

\end{axis}
\end{tikzpicture}
```

### Pattern 13: Heatmap

```latex
\begin{tikzpicture}
\begin{axis}[
  colorbar,
  colormap/viridis,
  xlabel=Feature 1,
  ylabel=Feature 2,
  width=8cm,
  height=8cm
]

\addplot[
  matrix plot*,
  point meta=explicit
] coordinates {
  (0,0) [0.1]  (1,0) [0.3]  (2,0) [0.5]
  (0,1) [0.4]  (1,1) [0.8]  (2,1) [0.6]
  (0,2) [0.7]  (1,2) [0.9]  (2,2) [0.4]
};

\end{axis}
\end{tikzpicture}
```

---

## Coordinate Systems

### Cartesian Coordinates

```latex
% Absolute coordinates
\draw (0,0) -- (2,3);

% Named coordinates
\coordinate (A) at (1,1);
\coordinate (B) at (3,2);
\draw (A) -- (B);

% Relative coordinates (from last point)
\draw (0,0) -- ++(1,0) -- ++(0,1) -- ++(-1,0) -- cycle;

% Polar coordinates (angle:radius)
\draw (0,0) -- (30:2);
\draw (0,0) -- (90:1.5);
```

### Coordinate Calculations

```latex
\usetikzlibrary{calc}

% Midpoint
\coordinate (mid) at ($(A)!0.5!(B)$);

% Point at 30% from A to B
\coordinate (c) at ($(A)!0.3!(B)$);

% Perpendicular point
\coordinate (d) at ($(A)!0.5!(B)!1cm!90:(B)$);

% Vector addition
\coordinate (e) at ($(A) + (B)$);

% Scaling
\coordinate (f) at ($(A)!2!(B)$);  % 2x distance from A through B
```

---

## LaTeX Integration

### Standalone TikZ Figure

```latex
\documentclass[tikz,border=2mm]{standalone}
\usepackage{tikz}
\usetikzlibrary{positioning,shapes,arrows.meta}

\begin{document}
\begin{tikzpicture}
  % Your diagram
  \node[circle,draw] {A};
\end{tikzpicture}
\end{document}
```

### In Academic Paper

```latex
\documentclass{article}
\usepackage{tikz}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}

\begin{document}

\begin{figure}[h]
  \centering
  \begin{tikzpicture}
    % Diagram code
  \end{tikzpicture}
  \caption{Neural network architecture.}
  \label{fig:network}
\end{figure}

\end{document}
```

### External TikZ File

```latex
% In main.tex
\begin{figure}[h]
  \centering
  \input{figures/network.tikz}
  \caption{My diagram.}
\end{figure}

% In figures/network.tikz
\begin{tikzpicture}
  \node[draw] {Content};
\end{tikzpicture}
```

---

## Complete Pattern Examples

### Example 1: Encoder-Decoder Architecture

```latex
\begin{tikzpicture}[
  rnn/.style={rectangle,draw,fill=blue!20,minimum width=1cm,minimum height=1.5cm},
  word/.style={rectangle,draw,fill=green!10,minimum width=1cm}
]

% Encoder
\foreach \i/\w in {0/The,1/cat,2/sat} {
  \node[word] (in\i) at (\i*2,0) {\w};
  \node[rnn] (enc\i) at (\i*2,1.5) {RNN};
  \draw[-Stealth] (in\i) -- (enc\i);

  \ifnum\i>0
    \draw[-Stealth] (enc\the\numexpr\i-1) -- (enc\i);
  \fi
}

% Context vector
\node[circle,draw,fill=yellow!20,minimum size=1cm] (ctx) at (3,3) {$c$};
\draw[-Stealth,thick] (enc2) -- (ctx);

% Decoder
\foreach \i/\w in {0/Le,1/chat,2/assis} {
  \node[rnn,fill=red!20] (dec\i) at (\i*2+6,1.5) {RNN};
  \node[word,fill=red!10] (out\i) at (\i*2+6,0) {\w};
  \draw[-Stealth] (dec\i) -- (out\i);

  \ifnum\i=0
    \draw[-Stealth,thick] (ctx) -- (dec0);
  \else
    \draw[-Stealth] (dec\the\numexpr\i-1) -- (dec\i);
  \fi
}

% Labels
\node[above=0.2cm of in1] {English};
\node[above=0.2cm of out1] {French};

\end{tikzpicture}
```

### Example 2: Attention Heatmap (TikZ Version)

```latex
\begin{tikzpicture}[
  scale=0.8,
  cell/.style={rectangle,minimum size=0.6cm,draw=white,line width=1pt}
]

% Define attention values (0-1)
\def\attn{
  {0.1,0.1,0.8},
  {0.2,0.7,0.1},
  {0.6,0.3,0.1}
}

% Draw heatmap
\foreach \row [count=\y] in \attn {
  \foreach \val [count=\x] in \row {
    \pgfmathsetmacro\shade{100*\val}
    \node[cell,fill=blue!\shade] at (\x,-\y) {};
  }
}

% Labels
\node at (1,-4) {The};
\node at (2,-4) {cat};
\node at (3,-4) {sat};

\node[rotate=90] at (0,-1) {The};
\node[rotate=90] at (0,-2) {cat};
\node[rotate=90] at (0,-3) {sat};

% Colorbar (simplified)
\foreach \i in {0,10,...,100} {
  \fill[blue!\i] (5,-3+\i/40) rectangle (5.3,-2.9+\i/40);
}
\node[right] at (5.3,-3) {0};
\node[right] at (5.3,-1) {1};

\end{tikzpicture}
```

### Example 3: ROC Curve

```latex
\begin{tikzpicture}
\begin{axis}[
  xlabel=False Positive Rate,
  ylabel=True Positive Rate,
  grid=major,
  legend pos=south east,
  xmin=0, xmax=1,
  ymin=0, ymax=1,
  width=8cm,
  height=8cm
]

% Random classifier baseline
\addplot[dashed,gray,thick] coordinates {(0,0) (1,1)};
\addlegendentry{Random (AUC=0.50)}

% Model ROC curve
\addplot[blue,thick,smooth] coordinates {
  (0,0) (0.05,0.6) (0.1,0.75) (0.2,0.85)
  (0.3,0.90) (0.5,0.95) (0.7,0.97) (1,1)
};
\addlegendentry{Our Model (AUC=0.92)}

% Perfect classifier reference
\addplot[red,thick,dotted] coordinates {(0,0) (0,1) (1,1)};
\addlegendentry{Perfect (AUC=1.00)}

\end{axis}
\end{tikzpicture}
```

---

## Best Practices

### Style Consistency

```latex
% Define custom styles at document level
\tikzset{
  mynode/.style={circle,draw,fill=blue!20,minimum size=0.8cm},
  myarrow/.style={-Stealth,thick},
  mylabel/.style={font=\small,above}
}

% Use consistently
\node[mynode] (A) at (0,0) {A};
\draw[myarrow] (A) -- (B);
```

### Scaling and Sizing

```latex
% Global scale
\begin{tikzpicture}[scale=0.8]
  % Content scales by 0.8
\end{tikzpicture}

% Transform canvas (affects everything)
\begin{tikzpicture}[transform canvas={scale=0.8}]
  % Even text scales
\end{tikzpicture}

% Better: Set explicit sizes
\begin{tikzpicture}[x=1cm,y=1cm]
  % 1 unit = 1cm
\end{tikzpicture}
```

### Performance Tips

```latex
% For complex plots, externalize TikZ compilation
\usetikzlibrary{external}
\tikzexternalize[prefix=tikz-cache/]

% Only recompile changed figures
```

---

## Quick Reference

```latex
% Basic template
\begin{tikzpicture}[
  node/.style={...},
  edge/.style={...}
]
  \node[node] (A) at (0,0) {A};
  \node[node] (B) at (2,1) {B};
  \draw[edge] (A) -- (B);
\end{tikzpicture}
```

**Next Steps:**
- See @scientificpaper:context/imaging/matplotlib-scientific.md for data plots
- See @scientificpaper:agents/figure-artist.md for AI-assisted generation
- See @scientificpaper:agents/latex-expert.md for compilation help
