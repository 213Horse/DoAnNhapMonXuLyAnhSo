# Sơ Đồ UML: Hệ Thống Nhận Dạng Biển Số Xe

## 1. Class Diagram

```mermaid
classDiagram
    class Main {
        +SCALAR_BLACK: tuple
        +SCALAR_WHITE: tuple
        +SCALAR_YELLOW: tuple
        +SCALAR_GREEN: tuple
        +SCALAR_RED: tuple
        +showSteps: bool
        +main(): void
        +drawRedRectangleAroundPlate(imgOriginalScene, licPlate): void
        +writeLicensePlateCharsOnImage(imgOriginalScene, licPlate): void
    }

    class Preprocess {
        +GAUSSIAN_SMOOTH_FILTER_SIZE: tuple
        +ADAPTIVE_THRESH_BLOCK_SIZE: int
        +ADAPTIVE_THRESH_WEIGHT: int
        +preprocess(imgOriginal): tuple
        +extractValue(imgOriginal): numpy.ndarray
        +maximizeContrast(imgGrayscale): numpy.ndarray
    }

    class DetectPlates {
        +PLATE_WIDTH_PADDING_FACTOR: float
        +PLATE_HEIGHT_PADDING_FACTOR: float
        +detectPlatesInScene(imgOriginalScene): list
        +findPossibleCharsInScene(imgThresh): list
        +extractPlate(imgOriginal, listOfMatchingChars): PossiblePlate
    }

    class DetectChars {
        +kNearest: cv2.ml.KNearest
        +MIN_PIXEL_WIDTH: int
        +MIN_PIXEL_HEIGHT: int
        +MIN_ASPECT_RATIO: float
        +MAX_ASPECT_RATIO: float
        +MIN_PIXEL_AREA: int
        +MIN_DIAG_SIZE_MULTIPLE_AWAY: float
        +MAX_DIAG_SIZE_MULTIPLE_AWAY: float
        +MAX_CHANGE_IN_AREA: float
        +MAX_CHANGE_IN_WIDTH: float
        +MAX_CHANGE_IN_HEIGHT: float
        +MAX_ANGLE_BETWEEN_CHARS: float
        +MIN_NUMBER_OF_MATCHING_CHARS: int
        +RESIZED_CHAR_IMAGE_WIDTH: int
        +RESIZED_CHAR_IMAGE_HEIGHT: int
        +MIN_CONTOUR_AREA: int
        +loadKNNDataAndTrainKNN(): bool
        +detectCharsInPlates(listOfPossiblePlates): list
        +findPossibleCharsInPlate(imgGrayscale, imgThresh): list
        +checkIfPossibleChar(possibleChar): bool
        +findListOfListsOfMatchingChars(listOfPossibleChars): list
        +findListOfMatchingChars(possibleChar, listOfChars): list
        +distanceBetweenChars(firstChar, secondChar): float
        +angleBetweenChars(firstChar, secondChar): float
        +removeInnerOverlappingChars(listOfMatchingChars): list
        +recognizeCharsInPlate(imgThresh, listOfMatchingChars): str
    }

    class PossiblePlate {
        +imgPlate: numpy.ndarray
        +imgGrayscale: numpy.ndarray
        +imgThresh: numpy.ndarray
        +rrLocationOfPlateInScene: tuple
        +strChars: str
        +__init__(): void
    }

    class PossibleChar {
        +contour: numpy.ndarray
        +boundingRect: tuple
        +intBoundingRectX: int
        +intBoundingRectY: int
        +intBoundingRectWidth: int
        +intBoundingRectHeight: int
        +intBoundingRectArea: int
        +intCenterX: int
        +intCenterY: int
        +fltDiagonalSize: float
        +fltAspectRatio: float
        +__init__(_contour): void
    }

    %% Relationships
    Main --> DetectPlates : uses
    Main --> DetectChars : uses
    Main --> Preprocess : uses
    Main --> PossiblePlate : creates
    
    DetectPlates --> Preprocess : uses
    DetectPlates --> DetectChars : uses
    DetectPlates --> PossiblePlate : creates
    DetectPlates --> PossibleChar : creates
    
    DetectChars --> Preprocess : uses
    DetectChars --> PossibleChar : uses
    DetectChars --> PossiblePlate : modifies
    
    Preprocess --> Main : provides preprocessing
```

## 2. Sequence Diagram - Luồng Xử Lý Chính

```mermaid
sequenceDiagram
    participant M as Main
    participant P as Preprocess
    participant DP as DetectPlates
    participant DC as DetectChars
    participant PP as PossiblePlate
    participant PC as PossibleChar

    M->>M: Load image (vin.jpg)
    M->>P: preprocess(imgOriginal)
    P->>P: extractValue()
    P->>P: maximizeContrast()
    P->>P: Gaussian blur
    P->>P: Adaptive threshold
    P-->>M: Return grayscale and threshold images
    
    M->>DP: detectPlatesInScene(imgOriginalScene)
    DP->>P: preprocess(imgOriginalScene)
    DP->>DP: findPossibleCharsInScene()
    DP->>PC: Create PossibleChar objects
    DP->>DC: findListOfListsOfMatchingChars()
    DP->>DP: extractPlate()
    DP->>PP: Create PossiblePlate objects
    DP-->>M: Return list of possible plates
    
    M->>DC: detectCharsInPlates(listOfPossiblePlates)
    loop For each possible plate
        DC->>P: preprocess(plate.imgPlate)
        DC->>DC: findPossibleCharsInPlate()
        DC->>DC: findListOfListsOfMatchingChars()
        DC->>DC: removeInnerOverlappingChars()
        DC->>DC: recognizeCharsInPlate()
        DC->>PP: Update strChars
    end
    DC-->>M: Return updated list of plates
    
    M->>M: Sort plates by character count
    M->>M: Select best plate
    M->>M: Draw results on image
    M->>M: Output license plate text
```

## 3. Activity Diagram - Quy Trình Xử Lý

```mermaid
flowchart TD
    A[Start] --> B[Load Image]
    B --> C[Preprocess Image]
    C --> D[Find All Contours]
    D --> E[Filter Possible Characters]
    E --> F[Group Matching Characters]
    F --> G[Extract Plate Regions]
    G --> H{Any Plates Found?}
    H -->|No| I[Output: No plates detected]
    H -->|Yes| J[Preprocess Plate Images]
    J --> K[Find Characters in Plates]
    K --> L[Group Characters in Plates]
    L --> M[Remove Overlapping Characters]
    M --> N[KNN Character Recognition]
    N --> O[Output License Plate Text]
    O --> P[Draw Results on Image]
    P --> Q[Save Output Image]
    Q --> R[End]
    I --> R
```

## 4. Component Diagram

```mermaid
graph TB
    subgraph "Input Layer"
        A[Image Input<br/>vin.jpg]
    end
    
    subgraph "Processing Layer"
        B[Preprocessing Module<br/>Preprocess.py]
        C[Plate Detection Module<br/>DetectPlates.py]
        D[Character Recognition Module<br/>DetectChars.py]
    end
    
    subgraph "Data Models"
        E[PossiblePlate Class<br/>PossiblePlate.py]
        F[PossibleChar Class<br/>PossibleChar.py]
    end
    
    subgraph "Training Data"
        G[classifications.txt]
        H[flattened_images.txt]
        I[KNN Model]
    end
    
    subgraph "Output Layer"
        J[Processed Image<br/>imgOriginalScene.png]
        K[License Plate Text<br/>Console Output]
    end
    
    A --> B
    B --> C
    C --> D
    C --> E
    D --> F
    D --> G
    D --> H
    D --> I
    D --> J
    D --> K
```

## 5. State Diagram - Trạng Thái Xử Lý

```mermaid
stateDiagram-v2
    [*] --> ImageLoaded
    ImageLoaded --> Preprocessed
    Preprocessed --> ContoursFound
    ContoursFound --> CharactersFiltered
    CharactersFiltered --> CharactersGrouped
    CharactersGrouped --> PlatesExtracted
    PlatesExtracted --> CharactersRecognized
    CharactersRecognized --> ResultsOutput
    ResultsOutput --> [*]
    
    state CharactersFiltered {
        [*] --> CheckingSize
        CheckingSize --> CheckingAspectRatio
        CheckingAspectRatio --> ValidCharacter
        ValidCharacter --> [*]
    }
    
    state CharactersRecognized {
        [*] --> KNNTraining
        KNNTraining --> CharacterClassification
        CharacterClassification --> TextAssembly
        TextAssembly --> [*]
    }
```

## 6. Data Flow Diagram

```mermaid
graph LR
    A[Input Image] --> B[Preprocessing]
    B --> C[Contour Detection]
    C --> D[Character Filtering]
    D --> E[Character Grouping]
    E --> F[Plate Extraction]
    F --> G[Plate Preprocessing]
    G --> H[Character Detection in Plate]
    H --> I[Character Recognition]
    I --> J[Output Text]
    
    K[Training Data] --> I
    L[KNN Model] --> I
    
    style A fill:#e1f5fe
    style J fill:#c8e6c9
    style K fill:#fff3e0
    style L fill:#fff3e0
```

## 7. Module Dependencies

```mermaid
graph TD
    A[Main.py] --> B[DetectPlates.py]
    A --> C[DetectChars.py]
    A --> D[Preprocess.py]
    A --> E[PossiblePlate.py]
    
    B --> D
    B --> C
    B --> E
    B --> F[PossibleChar.py]
    
    C --> D
    C --> F
    C --> G[classifications.txt]
    C --> H[flattened_images.txt]
    
    D --> I[OpenCV]
    D --> J[NumPy]
    
    C --> I
    C --> J
    C --> K[KNN Algorithm]
    
    style A fill:#ffcdd2
    style B fill:#c8e6c9
    style C fill:#c8e6c9
    style D fill:#c8e6c9
    style E fill:#fff9c4
    style F fill:#fff9c4
``` 