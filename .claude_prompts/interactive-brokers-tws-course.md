# Interactive Brokers Trader Workstation (TWS) Comprehensive Course

## Course Overview

Create a complete, structured educational course for mastering Interactive Brokers Trader Workstation (TWS). This course should take learners from complete beginner to expert-level proficiency through progressive modules, hands-on exercises, real-world scenarios, and skill assessments.

---

## Course Design Principles

### Pedagogical Framework
- **Scaffolded Learning**: Each module builds on previous knowledge
- **Active Learning**: Hands-on exercises after every concept
- **Spaced Repetition**: Key concepts reinforced across modules
- **Mastery-Based Progression**: Clear competency checkpoints
- **Real-World Application**: Practical scenarios throughout

### Learning Modalities
- **Visual**: Screenshots, diagrams, flowcharts, video placeholders
- **Kinesthetic**: Step-by-step exercises, simulations, practice trades
- **Conceptual**: Theory explanations, mental models, decision frameworks
- **Assessment**: Quizzes, practical tests, capstone projects

---

## Course Structure

```
COURSE ARCHITECTURE:
├── Foundation Track (Modules 1-3)
│   └── Beginner Level: Platform basics, navigation, simple orders
├── Core Competency Track (Modules 4-7)
│   └── Intermediate Level: All trading views, order types, analysis tools
├── Advanced Track (Modules 8-11)
│   └── Advanced Level: Options, risk management, automation
├── Mastery Track (Modules 12-14)
│   └── Expert Level: Professional setups, optimization, integration
└── Capstone Projects
    └── Real-world trading scenarios and assessments
```

---

## MODULE 1: Platform Foundations

### Learning Objectives
By the end of this module, learners will be able to:
- Install and configure TWS for first use
- Navigate the main interface components confidently
- Understand account structure and permissions
- Execute basic platform operations

### Lesson 1.1: Introduction to TWS
```
CONTENT REQUIREMENTS:
├── What is TWS?
│   ├── Platform positioning in trading ecosystem
│   ├── TWS vs competitors (ThinkOrSwim, TradeStation, etc.)
│   ├── TWS Desktop vs TWS Web vs IBKR Mobile
│   └── When to use each platform variant
├── Platform Architecture
│   ├── Java-based application explained
│   ├── Client-server model
│   ├── Data streaming architecture
│   └── Order routing system overview
├── System Requirements
│   ├── Minimum vs recommended specs
│   ├── Operating system considerations
│   ├── Network requirements
│   └── Multi-monitor support
└── Visual Aid: Platform comparison matrix
```

**Exercise 1.1**: Download and install TWS on your system. Document the installation steps and any configuration choices made.

### Lesson 1.2: Account Setup and Security
```
CONTENT REQUIREMENTS:
├── Account Types Deep Dive
│   ├── Individual accounts
│   ├── Joint accounts
│   ├── IRA accounts
│   ├── Entity accounts
│   └── Paper trading accounts
├── Security Configuration
│   ├── Two-factor authentication (IB Key, SMS, hardware token)
│   ├── Security device setup walkthrough
│   ├── Trusted devices management
│   └── Session timeout settings
├── Trading Permissions
│   ├── Asset class permissions
│   ├── Market data permissions
│   ├── Margin permissions
│   └── How to request additional permissions
└── Visual Aid: Security setup flowchart
```

**Exercise 1.2**: Set up two-factor authentication and configure your paper trading account. Test login from a new device.

### Lesson 1.3: Interface Overview
```
CONTENT REQUIREMENTS:
├── Main Window Anatomy
│   ├── Title bar (account info, connection status)
│   ├── Menu bar (each menu explained)
│   ├── Toolbar (customization options)
│   ├── Main workspace area
│   └── Status bar (connection, alerts, bulletins)
├── First Launch Experience
│   ├── Default layout explanation
│   ├── Welcome wizard options
│   ├── Initial settings recommendations
│   └── Paper trading mode activation
├── Interface Themes
│   ├── Light vs dark mode
│   ├── Color customization
│   └── Font settings
└── Visual Aid: Annotated screenshot of main window with numbered callouts
```

**Exercise 1.3**: Identify and label all main interface components. Change the color theme and customize the toolbar.

### Lesson 1.4: Basic Navigation
```
CONTENT REQUIREMENTS:
├── Menu System Navigation
│   ├── File menu operations
│   ├── Edit menu functions
│   ├── View menu options
│   ├── Trading menu access
│   ├── Analytics menu tools
│   ├── Tools menu utilities
│   └── Window and Help menus
├── Symbol Entry Methods
│   ├── Quick symbol search
│   ├── Contract search dialog
│   ├── Exchange selection
│   └── Currency considerations
├── Keyboard Navigation
│   ├── Essential shortcuts (10 must-know)
│   ├── Tab navigation
│   ├── Quick access keys
│   └── Search functionality (Ctrl+F)
└── Visual Aid: Navigation flowchart and shortcut reference card
```

**Exercise 1.4**: Navigate to find the following using only keyboard shortcuts: (1) Account summary, (2) AAPL option chain, (3) EUR/USD forex quote, (4) Market scanner.

### Module 1 Assessment
```
QUIZ (20 questions):
├── Multiple choice on interface components
├── True/false on security best practices
├── Matching: Menu items to their functions
└── Short answer: Navigation scenarios

PRACTICAL TEST:
├── Configure TWS from scratch
├── Set up security properly
├── Navigate to 5 specified locations within time limit
└── Customize interface per given specifications
```

---

## MODULE 2: Mosaic Workspace Mastery

### Learning Objectives
- Create and customize Mosaic workspaces
- Configure all standard Mosaic windows
- Link windows effectively for workflow efficiency
- Save and manage multiple workspace layouts

### Lesson 2.1: Mosaic Philosophy and Architecture
```
CONTENT REQUIREMENTS:
├── Mosaic Design Philosophy
│   ├── Modular workspace concept
│   ├── Information density optimization
│   ├── Workflow-centric design
│   └── Mosaic vs Classic: Decision framework
├── Default Mosaic Layout
│   ├── Component identification
│   ├── Default window purposes
│   ├── Standard configurations
│   └── Why defaults matter
├── Workspace Management
│   ├── Creating new workspaces
│   ├── Switching between workspaces
│   ├── Workspace naming conventions
│   └── Backup and restore
└── Visual Aid: Default Mosaic layout annotated diagram
```

**Exercise 2.1**: Create three different workspaces named "Research", "Trading", and "Monitoring". Switch between them efficiently.

### Lesson 2.2: Watchlist Configuration
```
CONTENT REQUIREMENTS:
├── Watchlist Fundamentals
│   ├── Creating watchlists
│   ├── Adding/removing symbols
│   ├── Organizing symbols (groups, folders)
│   └── Multiple watchlist management
├── Column Configuration (COMPREHENSIVE)
│   ├── Price columns (Last, Bid, Ask, Open, High, Low, Close)
│   ├── Change columns (Change, % Change, from Open)
│   ├── Volume columns (Volume, Avg Volume, Relative Volume)
│   ├── Fundamental columns (P/E, Market Cap, Dividend Yield)
│   ├── Technical columns (52-week High/Low, RSI, Moving Averages)
│   ├── Options columns (IV, IV Rank, Next Earnings)
│   └── Custom column creation
├── Conditional Formatting
│   ├── Color coding by value
│   ├── Alert highlighting
│   ├── Threshold-based formatting
│   └── Custom formatting rules
├── Advanced Features
│   ├── Sorting (single and multi-column)
│   ├── Filtering
│   ├── Import/Export (CSV format)
│   └── Watchlist templates
└── Visual Aid: Before/after watchlist customization screenshots
```

**Exercise 2.2**: Create a watchlist with 20 stocks. Configure columns for: Last, Change%, Volume, 52wk High, P/E, IV Rank. Apply color coding for gainers (green) and losers (red). Export to CSV.

### Lesson 2.3: Order Entry Panel
```
CONTENT REQUIREMENTS:
├── Panel Layout
│   ├── Symbol selection area
│   ├── Order type selector
│   ├── Quantity input
│   ├── Price fields (limit, stop, etc.)
│   ├── Time in force selector
│   └── Transmit button
├── Order Entry Workflow
│   ├── Step-by-step order creation
│   ├── Order preview functionality
│   ├── Modification before transmission
│   └── Confirmation settings
├── Quick Order Features
│   ├── Quantity shortcuts (hotkeys)
│   ├── Price shortcuts (bid, ask, last, mid)
│   ├── Order templates
│   └── One-click order modes
├── Order Panel Customization
│   ├── Default order settings
│   ├── Panel layout options
│   ├── Preset configurations
│   └── Symbol-specific defaults
└── Visual Aid: Order entry workflow diagram
```

**Exercise 2.3**: Place the following paper trades using the Order Entry Panel:
1. Market buy 100 shares of SPY
2. Limit buy 50 shares of AAPL at $5 below current price
3. Stop loss sell for your SPY position at 2% below entry

### Lesson 2.4: Monitor Panels
```
CONTENT REQUIREMENTS:
├── Activity Monitor
│   ├── Live activity feed
│   ├── Activity types displayed
│   ├── Filtering options
│   └── Time range settings
├── Portfolio Monitor
│   ├── Position display
│   ├── P&L columns (unrealized, realized, total)
│   ├── Greeks display (for options)
│   ├── Cost basis information
│   └── Position grouping options
├── Orders Monitor
│   ├── Working orders display
│   ├── Order status indicators
│   ├── Order modification from monitor
│   ├── Order cancellation
│   └── Filled orders history
├── Trades Monitor
│   ├── Execution display
│   ├── Fill details
│   ├── Execution quality metrics
│   └── Export functionality
└── Visual Aid: Four-panel monitor layout screenshot
```

**Exercise 2.4**: Execute 5 trades and track them through all four monitors. Document the order lifecycle from submission to fill.

### Lesson 2.5: Charts in Mosaic
```
CONTENT REQUIREMENTS:
├── Chart Window Basics
│   ├── Adding chart to Mosaic
│   ├── Chart sizing and positioning
│   ├── Multiple chart arrangements
│   └── Chart linking to watchlist
├── Essential Chart Configuration
│   ├── Time frame selection
│   ├── Chart type selection
│   ├── Price scale options
│   ├── Volume display
│   └── Grid and crosshair settings
├── Quick Indicator Addition
│   ├── Most common indicators
│   ├── Indicator parameters
│   ├── Multiple indicators
│   └── Indicator templates
├── Basic Drawing Tools
│   ├── Trend lines
│   ├── Horizontal lines (support/resistance)
│   ├── Text annotations
│   └── Saving drawings
└── Visual Aid: Chart configuration step-by-step screenshots
```

**Exercise 2.5**: Set up a 4-chart grid showing SPY on Daily, 4H, 1H, and 15min timeframes. Add 20 EMA and 50 EMA to each. Draw support/resistance lines on the daily chart.

### Lesson 2.6: Window Linking
```
CONTENT REQUIREMENTS:
├── Link Groups Concept
│   ├── Color-coded link groups
│   ├── How linking works
│   ├── Link group management
│   └── Independent vs linked windows
├── Linking Configuration
│   ├── Setting link color
│   ├── Adding windows to groups
│   ├── Breaking links
│   └── Multiple link groups
├── Effective Linking Strategies
│   ├── Watchlist-to-chart linking
│   ├── Watchlist-to-order-panel linking
│   ├── Multi-chart synchronization
│   └── Cross-workspace linking
├── Troubleshooting Links
│   ├── Common linking issues
│   ├── Link not working solutions
│   └── Reset link groups
└── Visual Aid: Linking workflow diagram with color coding
```

**Exercise 2.6**: Create a linked workflow: Watchlist (blue) → Chart (blue) → Order Panel (blue). Verify that clicking a symbol in the watchlist updates both the chart and order panel.

### Lesson 2.7: Layout Management
```
CONTENT REQUIREMENTS:
├── Saving Layouts
│   ├── Save current layout
│   ├── Save as new layout
│   ├── Layout naming best practices
│   └── Auto-save settings
├── Loading Layouts
│   ├── Quick layout switch
│   ├── Layout library
│   ├── Default layout setting
│   └── Startup layout configuration
├── Layout Organization
│   ├── Layout categories
│   ├── Sharing layouts
│   ├── Import/export layouts
│   └── Backup strategies
├── Multi-Monitor Layouts
│   ├── Span across monitors
│   ├── Per-monitor layouts
│   ├── Monitor detection
│   └── Layout restoration after disconnect
└── Visual Aid: Layout management interface walkthrough
```

**Exercise 2.7**: Create and save three complete layouts: "Morning Research", "Active Trading", "End of Day Review". Configure each with appropriate windows and settings for its purpose.

### Module 2 Assessment
```
QUIZ (25 questions):
├── Watchlist configuration scenarios
├── Order panel feature identification
├── Monitor panel purposes
├── Linking troubleshooting scenarios
└── Layout management best practices

PRACTICAL TEST:
├── Build a complete Mosaic workspace from scratch
├── Configure watchlist with 15 specific columns
├── Set up linked chart + order panel workflow
├── Save and restore layout successfully
└── Time limit: 20 minutes
```

---

## MODULE 3: Classic TWS Proficiency

### Learning Objectives
- Navigate and customize Classic TWS Quote Monitor
- Configure pages and tabs effectively
- Set up hot buttons for rapid execution
- Understand when Classic TWS is preferable

### Lesson 3.1: Classic TWS vs Mosaic
```
CONTENT REQUIREMENTS:
├── Architectural Differences
│   ├── Single-window vs multi-window design
│   ├── Data density comparison
│   ├── Performance characteristics
│   └── Resource usage differences
├── Use Case Decision Framework
│   ├── When Classic is better
│   │   ├── High-frequency monitoring
│   │   ├── Limited screen real estate
│   │   ├── Data-dense workflows
│   │   └── Legacy compatibility
│   ├── When Mosaic is better
│   │   ├── Multi-monitor setups
│   │   ├── Visual-heavy workflows
│   │   ├── Flexible arrangements
│   │   └── Modern workflows
│   └── Hybrid approaches
├── Switching Between Modes
│   ├── Mode toggle location
│   ├── Settings preservation
│   └── Layout considerations
└── Visual Aid: Side-by-side comparison with annotations
```

**Exercise 3.1**: Switch between Mosaic and Classic TWS. Document three scenarios where each would be preferable based on your observations.

### Lesson 3.2: Quote Monitor Pages
```
CONTENT REQUIREMENTS:
├── Page Architecture
│   ├── Tab-based organization
│   ├── Page types (trading page, portfolio page, etc.)
│   ├── Page limits and considerations
│   └── Page hierarchy
├── Creating and Managing Pages
│   ├── New page creation
│   ├── Page naming
│   ├── Page duplication
│   ├── Page deletion
│   └── Page reordering
├── Page Templates
│   ├── Built-in templates
│   ├── Custom template creation
│   ├── Template sharing
│   └── Template best practices
├── Page Organization Strategies
│   ├── By asset class
│   ├── By strategy
│   ├── By watchlist type
│   └── By workflow stage
└── Visual Aid: Page management interface screenshots
```

**Exercise 3.2**: Create a page structure with: (1) Tech Stocks page, (2) ETFs page, (3) Options page, (4) Forex page. Add 10 appropriate symbols to each.

### Lesson 3.3: Column Configuration in Classic
```
CONTENT REQUIREMENTS:
├── Available Columns (COMPREHENSIVE LIST)
│   ├── Market Data Columns
│   │   ├── Bid/Ask/Last
│   │   ├── Bid Size/Ask Size
│   │   ├── High/Low/Open/Close
│   │   ├── Volume/Average Volume
│   │   └── VWAP
│   ├── Change Columns
│   │   ├── Change (absolute)
│   │   ├── Change (percentage)
│   │   ├── Change from Open
│   │   └── Change from Close
│   ├── Position Columns
│   │   ├── Position
│   │   ├── Average Cost
│   │   ├── Unrealized P&L
│   │   ├── Realized P&L
│   │   └── Market Value
│   ├── Options-Specific Columns
│   │   ├── Implied Volatility
│   │   ├── Delta/Gamma/Theta/Vega
│   │   ├── Days to Expiration
│   │   └── Model Price
│   └── Fundamental Columns
│       ├── P/E Ratio
│       ├── EPS
│       ├── Market Cap
│       └── Dividend Yield
├── Column Configuration
│   ├── Adding columns
│   ├── Removing columns
│   ├── Reordering columns
│   ├── Column width adjustment
│   └── Column presets
├── Custom Columns
│   ├── Calculated columns
│   ├── Formula syntax
│   └── Custom column examples
└── Visual Aid: Column configuration dialog walkthrough
```

**Exercise 3.3**: Configure a Quote Monitor page with exactly these columns in order: Symbol, Last, Change%, Bid, Ask, Volume, 52W High, 52W Low, P/E, Position, Unrealized P&L. Save as a template.

### Lesson 3.4: Hot Buttons
```
CONTENT REQUIREMENTS:
├── Hot Button Concepts
│   ├── What hot buttons do
│   ├── Placement options
│   ├── Action types available
│   └── Execution behavior
├── Creating Hot Buttons
│   ├── Button creation wizard
│   ├── Action configuration
│   ├── Button labeling
│   ├── Color coding
│   └── Icon selection
├── Common Hot Button Configurations
│   ├── Buy Market
│   ├── Sell Market
│   ├── Buy Limit (at bid)
│   ├── Sell Limit (at ask)
│   ├── Cancel All Orders
│   ├── Flatten Position
│   ├── Close All Positions
│   └── Custom order buttons
├── Hot Button Management
│   ├── Editing buttons
│   ├── Rearranging buttons
│   ├── Deleting buttons
│   ├── Button groups
│   └── Import/Export buttons
├── Safety Considerations
│   ├── Confirmation settings
│   ├── Accidental click prevention
│   ├── Testing in paper trading
│   └── Emergency stop buttons
└── Visual Aid: Hot button creation step-by-step
```

**Exercise 3.4**: Create a hot button bar with: (1) Buy 100 Market, (2) Sell 100 Market, (3) Buy 100 Limit at Bid, (4) Sell 100 Limit at Ask, (5) Cancel All, (6) Close Position. Test each in paper trading.

### Lesson 3.5: Order Entry from Quote Monitor
```
CONTENT REQUIREMENTS:
├── Click Trading
│   ├── Single-click order creation
│   ├── Click locations (bid vs ask)
│   ├── Order line display
│   ├── Order modification on line
│   └── Transmit methods
├── Order Line Features
│   ├── Order status indicators
│   ├── Inline editing
│   ├── Right-click options
│   └── Multiple order lines
├── Bracket Orders from Quote Line
│   ├── Attaching profit target
│   ├── Attaching stop loss
│   ├── Bracket order templates
│   └── OCA group creation
├── Order Defaults for Quote Monitor
│   ├── Default order type
│   ├── Default quantity
│   ├── Default time in force
│   └── Symbol-specific defaults
└── Visual Aid: Order creation from quote line sequence
```

**Exercise 3.5**: Using only the Quote Monitor (no Order Entry Panel), execute the following sequence:
1. Create a limit buy order by clicking the bid
2. Modify the order price by 0.10
3. Attach a bracket (profit target +2%, stop loss -1%)
4. Transmit the order

### Module 3 Assessment
```
QUIZ (20 questions):
├── Classic vs Mosaic decision scenarios
├── Page management questions
├── Column identification
├── Hot button configuration
└── Order entry methods

PRACTICAL TEST:
├── Build complete Classic TWS setup
├── Create 5 organized pages
├── Configure comprehensive column layout
├── Set up 8 hot buttons with specific functions
├── Execute 10 trades using different methods
└── Time limit: 30 minutes
```

---

## MODULE 4: Order Types Mastery

### Learning Objectives
- Understand and correctly use all basic order types
- Configure conditional and advanced orders
- Select appropriate order types for different scenarios
- Manage and modify working orders effectively

### Lesson 4.1: Market Orders
```
CONTENT REQUIREMENTS:
├── Standard Market Order
│   ├── How market orders work
│   ├── Execution guarantee vs price guarantee
│   ├── Slippage explained
│   ├── When to use market orders
│   └── Risks of market orders
├── Market Order Variants
│   ├── Market on Open (MOO)
│   │   ├── How it works
│   │   ├── Auction participation
│   │   ├── Timing requirements
│   │   └── Use cases
│   ├── Market on Close (MOC)
│   │   ├── How it works
│   │   ├── Cutoff times
│   │   ├── Imbalance information
│   │   └── Use cases
│   └── Market if Touched (MIT)
│       ├── Trigger mechanics
│       ├── vs Stop orders
│       └── Use cases
├── Market Order Configuration in TWS
│   ├── Selecting market order type
│   ├── Quantity settings
│   ├── Time in force options
│   └── Transmit process
└── Visual Aid: Market order execution diagram
```

**Exercise 4.1**: Execute the following market orders in paper trading:
1. Market buy 50 shares during regular hours
2. Market buy 50 shares in pre-market (observe difference)
3. Set up a MOC order for end of day
4. Create a MIT order triggered at a specific price

### Lesson 4.2: Limit Orders
```
CONTENT REQUIREMENTS:
├── Standard Limit Order
│   ├── How limit orders work
│   ├── Price guarantee vs execution guarantee
│   ├── Limit order priority (price-time)
│   ├── Partial fills
│   └── When limit orders are essential
├── Limit Order Variants
│   ├── Limit on Open (LOO)
│   ├── Limit on Close (LOC)
│   ├── Limit if Touched (LIT)
│   └── Marketable limit orders
├── Limit Order Strategies
│   ├── Buying below market (support levels)
│   ├── Selling above market (resistance levels)
│   ├── Capturing spreads
│   └── Queue positioning
├── Limit Order Configuration
│   ├── Price entry methods
│   ├── Offset from current price
│   ├── Limit price shortcuts
│   └── Default limit offset setting
└── Visual Aid: Limit order placement scenarios
```

**Exercise 4.2**: Practice limit order scenarios:
1. Place limit buy 5% below current price (GTC)
2. Place limit sell 5% above current price (GTC)
3. Place a marketable limit buy (limit at ask)
4. Observe partial fill behavior with large quantity

### Lesson 4.3: Stop Orders
```
CONTENT REQUIREMENTS:
├── Stop Order (Stop Loss)
│   ├── Trigger mechanism
│   ├── Stop becomes market order
│   ├── Gap risk
│   └── Stop hunting concept
├── Stop Limit Order
│   ├── Two-price mechanism
│   ├── Stop price vs limit price
│   ├── Gap protection vs fill risk
│   └── When to use stop limit
├── Trailing Stop Orders
│   ├── Trailing amount (fixed vs percentage)
│   ├── Trail mechanics
│   ├── Activation rules
│   └── Best practices for trail amount
├── Trailing Stop Limit
│   ├── Combined mechanics
│   ├── Configuration options
│   └── Use cases
├── Stop with Protection (IBKR specific)
│   ├── How protection works
│   ├── Protection range settings
│   └── When to use
└── Visual Aid: Stop order trigger and execution diagrams
```

**Exercise 4.3**: Set up the following protective stops on an existing position:
1. Simple stop loss at -3%
2. Stop limit at -3% with 0.50 limit offset
3. Trailing stop at $2.00 trail amount
4. Trailing stop at 2% trail percentage

### Lesson 4.4: Conditional Orders
```
CONTENT REQUIREMENTS:
├── Bracket Orders
│   ├── Structure (entry + profit target + stop loss)
│   ├── Creating brackets
│   │   ├── From order panel
│   │   ├── From quote line
│   │   └── Attach to existing order
│   ├── Bracket templates
│   ├── Modifying bracket components
│   └── Risk/reward visualization
├── One-Cancels-All (OCA)
│   ├── OCA concept
│   ├── Creating OCA groups
│   ├── Manual OCA grouping
│   ├── OCA with brackets
│   └── OCA management
├── Conditional Orders (If...Then)
│   ├── Condition types
│   │   ├── Price conditions
│   │   ├── Time conditions
│   │   ├── Volume conditions
│   │   ├── Margin conditions
│   │   └── Execution conditions
│   ├── Creating conditional orders
│   ├── Multiple conditions (AND/OR)
│   └── Testing conditions
├── Order Chain (Sequence)
│   ├── Sequential order execution
│   ├── Creating order chains
│   └── Use cases
└── Visual Aid: Conditional order logic flowcharts
```

**Exercise 4.4**: Create the following conditional setups:
1. Bracket order with 2:1 reward/risk ratio
2. OCA group with 3 different limit buy orders
3. Conditional order that triggers when SPY > $450
4. Order chain: Buy 100 shares, then immediately place stop loss

### Lesson 4.5: Advanced Order Types
```
CONTENT REQUIREMENTS:
├── Iceberg/Reserve Orders
│   ├── Display quantity concept
│   ├── Reserve quantity
│   ├── Refill logic
│   ├── Use cases (large orders)
│   └── Configuration in TWS
├── Pegged Orders
│   ├── Pegged to Market
│   ├── Pegged to Midpoint
│   ├── Pegged to Best
│   ├── Pegged to Primary
│   └── Offset configuration
├── Relative Orders
│   ├── Relative order mechanics
│   ├── Offset from NBBO
│   ├── Cap price
│   └── Use cases
├── Discretionary Orders
│   ├── Discretionary amount
│   ├── How it works
│   └── When to use
├── Hidden Orders
│   ├── How hidden orders work
│   ├── Exchange support
│   └── Limitations
└── Visual Aid: Advanced order type comparison matrix
```

**Exercise 4.5**: Execute the following advanced orders:
1. Iceberg buy 1000 shares, showing only 100 at a time
2. Pegged to midpoint buy order
3. Relative buy order with 0.05 offset

### Lesson 4.6: Algorithmic Orders (IB Algos)
```
CONTENT REQUIREMENTS:
├── Algorithm Overview
│   ├── Why use algorithms
│   ├── Available IB algorithms
│   └── Algorithm selection framework
├── VWAP (Volume-Weighted Average Price)
│   ├── VWAP concept
│   ├── Start/end time configuration
│   ├── Max percentage of volume
│   ├── Use cases
│   └── Performance benchmarking
├── TWAP (Time-Weighted Average Price)
│   ├── TWAP concept
│   ├── Time slice configuration
│   ├── Randomization options
│   └── Use cases
├── Arrival Price
│   ├── Concept and goal
│   ├── Urgency settings
│   ├── Risk aversion parameters
│   └── When to use
├── Adaptive Algorithm
│   ├── How adaptive works
│   ├── Priority settings (patient to urgent)
│   ├── Best use cases
│   └── Performance expectations
├── Accumulate/Distribute
│   ├── Multi-day execution
│   ├── Component orders
│   ├── Randomization
│   └── Large position building
├── Other Algorithms
│   ├── Close Price
│   ├── Balance Impact & Risk
│   ├── Minimize Impact
│   ├── Percentage of Volume
│   └── Target Close
└── Visual Aid: Algorithm selection decision tree
```

**Exercise 4.6**: Execute algorithmic orders:
1. VWAP buy 500 shares over 2 hours
2. Adaptive buy 200 shares with "Patient" priority
3. Compare fills and prices to market orders

### Module 4 Assessment
```
QUIZ (30 questions):
├── Order type identification from descriptions
├── Scenario-based order type selection
├── Order attribute configuration
├── Algorithm selection scenarios
└── Risk assessment for order types

PRACTICAL TEST:
├── Execute all basic order types correctly
├── Set up complex bracket with OCA
├── Create multi-condition conditional order
├── Execute algorithm order and track performance
├── Modify and cancel orders efficiently
└── Time limit: 45 minutes
```

---

## MODULE 5: OptionTrader Comprehensive

### Learning Objectives
- Navigate option chains efficiently
- Understand and interpret Greeks
- Build and execute option strategies
- Manage option positions effectively

### Lesson 5.1: Option Chain Navigation
```
CONTENT REQUIREMENTS:
├── Accessing OptionTrader
│   ├── From menu
│   ├── From watchlist
│   ├── From chart
│   └── Keyboard shortcut
├── Option Chain Layout
│   ├── Underlying quote section
│   ├── Expiration selection (tabs/dropdown)
│   ├── Strike price display
│   ├── Call side vs Put side
│   └── Chain width settings
├── Chain Configuration
│   ├── Strike range display
│   ├── Strike increment settings
│   ├── Near-the-money centering
│   ├── Show all vs filtered strikes
│   └── Multi-expiration view
├── Chain Columns
│   ├── Bid/Ask/Last/Volume
│   ├── Open Interest
│   ├── Implied Volatility
│   ├── Greeks columns
│   └── Custom column arrangement
└── Visual Aid: Annotated option chain screenshot
```

**Exercise 5.1**: Navigate to AAPL options. Configure the chain to show: strikes within $10 of ATM, columns for Bid, Ask, IV, Delta, Open Interest. Find the ATM options for the nearest monthly expiration.

### Lesson 5.2: Understanding Greeks Display
```
CONTENT REQUIREMENTS:
├── Delta
│   ├── Definition and calculation
│   ├── Delta as directional exposure
│   ├── Delta as probability proxy
│   ├── Delta display in TWS
│   └── Delta interpretation examples
├── Gamma
│   ├── Definition and calculation
│   ├── Gamma risk
│   ├── Gamma and time to expiration
│   ├── Gamma display in TWS
│   └── Gamma interpretation
├── Theta
│   ├── Definition and calculation
│   ├── Time decay visualization
│   ├── Theta acceleration
│   ├── Theta display in TWS
│   └── Theta implications for strategies
├── Vega
│   ├── Definition and calculation
│   ├── Volatility sensitivity
│   ├── Vega and expiration
│   ├── Vega display in TWS
│   └── Trading volatility
├── Rho
│   ├── Definition and significance
│   ├── Interest rate sensitivity
│   └── When rho matters
├── Position Greeks
│   ├── Aggregate portfolio Greeks
│   ├── Greeks in Portfolio window
│   └── Risk management with Greeks
└── Visual Aid: Greeks sensitivity charts
```

**Exercise 5.2**: For a selected option position, record all Greeks and explain what each means for the position. Predict how P&L would change for: (1) $1 stock move up, (2) 5% IV increase, (3) 7 days passing.

### Lesson 5.3: Single-Leg Option Orders
```
CONTENT REQUIREMENTS:
├── Buying Calls
│   ├── When to buy calls
│   ├── Strike selection criteria
│   ├── Expiration selection
│   ├── Order entry process
│   └── Risk/reward analysis
├── Buying Puts
│   ├── When to buy puts
│   ├── Protective puts
│   ├── Speculative puts
│   └── Order entry process
├── Selling Calls
│   ├── Covered calls
│   ├── Naked calls (risks!)
│   ├── Strike selection for income
│   └── Assignment considerations
├── Selling Puts
│   ├── Cash-secured puts
│   ├── Naked puts
│   ├── Strike selection
│   └── Assignment as feature
├── Order Entry for Options
│   ├── From option chain
│   ├── Quantity (contracts)
│   ├── Limit orders for options
│   └── Bid/ask spread considerations
└── Visual Aid: Option P&L diagrams for each type
```

**Exercise 5.3**: Execute in paper trading:
1. Buy 1 ATM call, 30 days out
2. Buy 1 OTM put (2 strikes out), 45 days out
3. Sell 1 covered call (if holding stock)
4. Sell 1 cash-secured put, 2 strikes OTM

### Lesson 5.4: Spread Strategies
```
CONTENT REQUIREMENTS:
├── Vertical Spreads
│   ├── Bull Call Spread
│   │   ├── Construction
│   │   ├── Max profit/loss calculation
│   │   ├── Breakeven
│   │   ├── TWS Strategy Builder entry
│   │   └── Use cases
│   ├── Bear Put Spread
│   │   ├── Construction
│   │   ├── P&L characteristics
│   │   └── TWS entry
│   ├── Bull Put Spread (Credit)
│   │   ├── Construction
│   │   ├── Premium collection
│   │   └── TWS entry
│   └── Bear Call Spread (Credit)
│       ├── Construction
│       └── TWS entry
├── Horizontal (Calendar) Spreads
│   ├── Construction
│   ├── Theta play
│   ├── IV considerations
│   └── TWS entry
├── Diagonal Spreads
│   ├── Construction
│   ├── Characteristics
│   └── TWS entry
├── Using Strategy Builder
│   ├── Accessing Strategy Builder
│   ├── Adding legs
│   ├── Leg ratios
│   ├── Strategy analysis
│   └── Order transmission
└── Visual Aid: Spread P&L diagrams
```

**Exercise 5.4**: Build and analyze (don't transmit yet):
1. Bull call spread ($5 wide)
2. Iron condor
3. Calendar spread
Record max profit, max loss, and breakevens for each.

### Lesson 5.5: Complex Multi-Leg Strategies
```
CONTENT REQUIREMENTS:
├── Straddles
│   ├── Long straddle construction
│   ├── Short straddle construction
│   ├── Breakeven calculation
│   ├── Use cases
│   └── TWS entry
├── Strangles
│   ├── Long strangle
│   ├── Short strangle
│   ├── Strike selection
│   └── TWS entry
├── Iron Condors
│   ├── Construction (4 legs)
│   ├── Wing width considerations
│   ├── Probability of profit
│   ├── Management rules
│   └── TWS entry
├── Butterflies
│   ├── Long butterfly (call/put)
│   ├── Construction
│   ├── P&L characteristics
│   └── TWS entry
├── Iron Butterflies
│   ├── Construction
│   ├── vs Iron Condor
│   └── TWS entry
├── Custom Strategies
│   ├── Building custom combos
│   ├── Ratio spreads
│   ├── Back spreads
│   └── Saving custom strategies
└── Visual Aid: Complex strategy P&L diagrams
```

**Exercise 5.5**: Execute in paper trading:
1. Short iron condor, 30 days out, collecting at least $1.00
2. Long straddle on earnings stock
3. Butterfly centered at current price

### Lesson 5.6: Option Position Management
```
CONTENT REQUIREMENTS:
├── Monitoring Option Positions
│   ├── Portfolio view for options
│   ├── Greeks monitoring
│   ├── P&L tracking
│   └── Days to expiration alerts
├── Rolling Options
│   ├── Roll concept
│   ├── Rolling up/down/out
│   ├── Roll dialog in TWS
│   ├── Cost to roll analysis
│   └── When to roll vs close
├── Adjusting Positions
│   ├── Adding legs
│   ├── Converting positions
│   ├── Legging in/out
│   └── Adjustment strategies
├── Closing Positions
│   ├── Close single leg
│   ├── Close spread
│   ├── Close at market vs limit
│   └── Partial closes
├── Assignment and Exercise
│   ├── Assignment notification
│   ├── Assignment fees
│   ├── Exercise process
│   ├── Exercise (don't sell) orders
│   └── Expiration settings
└── Visual Aid: Position management workflows
```

**Exercise 5.6**: Practice position management:
1. Roll a short put to the next month
2. Convert a long call to a call spread
3. Close half of a multi-leg position

### Module 5 Assessment
```
QUIZ (35 questions):
├── Option chain navigation
├── Greeks interpretation scenarios
├── Strategy construction
├── P&L and breakeven calculations
└── Position management decisions

PRACTICAL TEST:
├── Navigate to specific options quickly
├── Build 3 different spread strategies
├── Calculate Greeks impact manually
├── Execute iron condor and manage it
├── Roll and adjust positions
└── Time limit: 45 minutes
```

---

## MODULE 6: Specialized Trading Views

### Learning Objectives
- Master FXTrader for currency trading
- Use BookTrader for scalping and Level II trading
- Configure ComboTrader for complex orders
- Implement BasketTrader for portfolio operations

### Lesson 6.1: FXTrader
```
CONTENT REQUIREMENTS:
├── FXTrader Interface
│   ├── Trading cells layout
│   ├── Currency pair display
│   ├── Bid/Ask presentation
│   ├── Spread display
│   └── Position information
├── Forex Trading Basics at IBKR
│   ├── Spot forex vs CFDs
│   ├── Currency pair notation
│   ├── Pip values
│   ├── Lot sizes
│   └── Trading hours
├── Order Entry in FXTrader
│   ├── Click trading
│   ├── Order types available
│   ├── Quantity specification
│   └── Limit vs market execution
├── FXTrader Configuration
│   ├── Displayed pairs
│   ├── Cell arrangement
│   ├── Color coding
│   └── Order defaults
├── Multi-Currency Considerations
│   ├── Base currency impact
│   ├── Conversion costs
│   ├── Currency exposure
│   └── Cash management
└── Visual Aid: FXTrader interface annotated
```

**Exercise 6.1**: Using FXTrader:
1. Configure 6 major currency pairs
2. Execute EUR/USD trade
3. Monitor position and P&L
4. Close position with limit order

### Lesson 6.2: BookTrader (Market Depth)
```
CONTENT REQUIREMENTS:
├── Level II Data Explained
│   ├── What is Level II
│   ├── Order book visualization
│   ├── Market makers/ECNs
│   └── Depth interpretation
├── BookTrader Interface
│   ├── Price ladder
│   ├── Bid column (size at each price)
│   ├── Ask column
│   ├── Your orders display
│   ├── Current position
│   └── P&L display
├── Trading from BookTrader
│   ├── Left-click actions (configurable)
│   ├── Right-click actions
│   ├── One-click trading
│   ├── Bracket orders
│   └── Order modification (drag)
├── BookTrader Hotkeys
│   ├── Buy at market
│   ├── Sell at market
│   ├── Buy at bid
│   ├── Sell at ask
│   ├── Cancel all
│   └── Flatten position
├── BookTrader Configuration
│   ├── Price increment settings
│   ├── Auto-centering
│   ├── Colors and fonts
│   ├── Sound alerts
│   └── Display depth
├── Scalping Setup with BookTrader
│   ├── Optimal configuration
│   ├── Hotkey setup
│   ├── Bracket defaults
│   └── Risk management
└── Visual Aid: BookTrader interface with trade examples
```

**Exercise 6.2**: Configure BookTrader for active trading:
1. Set up price ladder for SPY
2. Configure one-click trading
3. Execute 5 round-trip trades
4. Use bracket orders for each trade

### Lesson 6.3: ComboTrader
```
CONTENT REQUIREMENTS:
├── ComboTrader Overview
│   ├── What are combination orders
│   ├── Supported instruments
│   ├── Combo vs multi-leg
│   └── Execution as single unit
├── Creating Combinations
│   ├── Stock + Option combos
│   │   ├── Covered call combo
│   │   ├── Protective put combo
│   │   └── Married put
│   ├── Option Spreads
│   │   ├── Any spread strategy
│   │   ├── Complex multi-leg
│   │   └── Ratio combinations
│   ├── Futures Spreads
│   │   ├── Calendar spreads
│   │   ├── Inter-commodity spreads
│   │   └── Butterfly spreads
│   ├── EFP (Exchange for Physical)
│   │   ├── Stock + Future combo
│   │   └── Use cases
│   └── Custom Combinations
│       ├── Any instrument mix
│       └── Creative strategies
├── Combo Order Entry
│   ├── Leg builder interface
│   ├── Ratio specification
│   ├── Side specification
│   ├── Net price entry
│   └── Order type selection
├── Combo Pricing and Execution
│   ├── Net debit/credit
│   ├── Leg pricing
│   ├── Smart routing for combos
│   └── Fill behavior
└── Visual Aid: ComboTrader interface walkthrough
```

**Exercise 6.3**: Using ComboTrader, create and execute:
1. Covered call combo (buy stock + sell call)
2. Bull call spread
3. Stock + future combo (if applicable)

### Lesson 6.4: BasketTrader
```
CONTENT REQUIREMENTS:
├── BasketTrader Overview
│   ├── Basket trading concepts
│   ├── Use cases
│   │   ├── Index replication
│   │   ├── Sector trades
│   │   ├── Portfolio rebalancing
│   │   └── Multi-name execution
│   └── Basket vs individual orders
├── Creating Baskets
│   ├── Manual entry
│   │   ├── Symbol input
│   │   ├── Quantity input
│   │   ├── Side specification
│   │   └── Order type per item
│   ├── Import from CSV/Excel
│   │   ├── File format requirements
│   │   ├── Column mapping
│   │   ├── Validation
│   │   └── Error handling
│   ├── Import from Portfolio
│   │   ├── Current positions
│   │   ├── Modification
│   │   └── Close all functionality
│   └── Basket Templates
│       ├── Saving baskets
│       ├── Loading baskets
│       └── Template management
├── Basket Order Configuration
│   ├── Order type (per basket or per item)
│   ├── Percentage allocation
│   ├── Dollar allocation
│   ├── Shares allocation
│   └── Execution timing
├── Basket Execution
│   ├── Preview orders
│   ├── Transmit all
│   ├── Selective transmission
│   └── Execution monitoring
├── Basket Analysis
│   ├── Total exposure calculation
│   ├── Commission estimate
│   ├── Sector breakdown
│   └── Risk metrics
└── Visual Aid: BasketTrader workflow screenshots
```

**Exercise 6.4**: Create and execute a sector basket:
1. Create basket with 5 tech stocks (equal weight)
2. Set order type to limit (at ask)
3. Preview total cost
4. Execute basket
5. Later, use BasketTrader to close all positions

### Lesson 6.5: Rebalance Portfolio Tool
```
CONTENT REQUIREMENTS:
├── Rebalance Tool Overview
│   ├── Purpose and benefits
│   ├── Accessing the tool
│   └── Prerequisites
├── Setting Target Allocations
│   ├── Percentage-based targets
│   ├── Dollar-based targets
│   ├── Share-based targets
│   └── Model portfolio import
├── Rebalance Analysis
│   ├── Current vs target comparison
│   ├── Required trades calculation
│   ├── Tax lot considerations
│   ├── Cash requirements
│   └── Commission impact
├── Generating Rebalance Orders
│   ├── Automatic order generation
│   ├── Order review
│   ├── Modification options
│   ├── Order type selection
│   └── Timing options
├── Execution and Monitoring
│   ├── Transmit orders
│   ├── Partial execution handling
│   ├── Rebalance status
│   └── Post-rebalance verification
└── Visual Aid: Rebalance workflow step-by-step
```

**Exercise 6.5**: Use the Rebalance tool:
1. Set target allocation: 40% SPY, 30% QQQ, 30% IWM
2. Review required trades
3. Execute rebalance
4. Verify final allocation

### Module 6 Assessment
```
QUIZ (25 questions):
├── FXTrader configuration
├── BookTrader trading scenarios
├── ComboTrader combination types
├── BasketTrader operations
└── Rebalance tool procedures

PRACTICAL TEST:
├── Execute forex trade via FXTrader
├── Complete 10 round-trips in BookTrader
├── Create and execute 3 combo orders
├── Build and execute portfolio basket
├── Rebalance to target allocation
└── Time limit: 40 minutes
```

---

## MODULE 7: Charts and Technical Analysis

### Learning Objectives
- Configure all chart types and time frames
- Apply and interpret 50+ technical indicators
- Use drawing tools for technical analysis
- Trade directly from charts

### Lesson 7.1: Chart Types and Configuration
```
CONTENT REQUIREMENTS:
├── Chart Types (COMPREHENSIVE)
│   ├── Candlestick Charts
│   │   ├── Anatomy of a candle
│   │   ├── Color configuration
│   │   ├── Common patterns
│   │   └── Best use cases
│   ├── OHLC Bar Charts
│   │   ├── Bar structure
│   │   ├── vs Candlesticks
│   │   └── Use cases
│   ├── Line Charts
│   │   ├── Close vs typical price
│   │   ├── Best for trends
│   │   └── Overlay usage
│   ├── Area Charts
│   │   ├── Fill options
│   │   └── Use cases
│   ├── Heikin-Ashi
│   │   ├── Calculation method
│   │   ├── Trend identification
│   │   └── Trading signals
│   ├── Renko Charts
│   │   ├── Box size configuration
│   │   ├── Trend focus
│   │   └── Use cases
│   ├── Kagi Charts
│   │   ├── Reversal amount
│   │   ├── Pattern reading
│   │   └── Traditional usage
│   └── Point and Figure
│       ├── Box size and reversal
│       ├── Pattern interpretation
│       └── Price targets
├── Time Frame Selection
│   ├── Tick charts
│   ├── Second charts (1s, 5s, 10s, 30s)
│   ├── Minute charts (1, 2, 3, 5, 10, 15, 30, 60)
│   ├── Hourly charts (2H, 4H)
│   ├── Daily, Weekly, Monthly
│   └── Custom time frames
├── Chart Settings
│   ├── Price scale (linear vs log)
│   ├── Time axis settings
│   ├── Grid display
│   ├── Crosshair options
│   ├── Session breaks
│   └── Extended hours display
└── Visual Aid: Chart type comparison grid
```

**Exercise 7.1**: Create a 4-chart layout comparing:
1. Candlestick daily chart
2. Heikin-Ashi daily chart
3. Renko chart (1% box)
4. Point and Figure chart
Analyze how each displays the same price action differently.

### Lesson 7.2: Moving Averages
```
CONTENT REQUIREMENTS:
├── Simple Moving Average (SMA)
│   ├── Calculation
│   ├── Common periods (10, 20, 50, 100, 200)
│   ├── Interpretation
│   ├── Crossover signals
│   └── Configuration in TWS
├── Exponential Moving Average (EMA)
│   ├── Calculation (smoothing factor)
│   ├── vs SMA comparison
│   ├── Common periods
│   └── Use cases
├── Weighted Moving Average (WMA)
│   ├── Calculation
│   ├── Use cases
│   └── Configuration
├── Volume-Weighted MA (VWMA)
│   ├── Calculation
│   ├── Interpretation
│   └── Comparison to VWAP
├── Moving Average Strategies
│   ├── Single MA trend
│   ├── Dual MA crossover
│   ├── Triple MA system
│   ├── MA as support/resistance
│   └── Golden/Death cross
├── TWS Configuration
│   ├── Adding MA to chart
│   ├── Period settings
│   ├── Source (close, typical, etc.)
│   ├── Color and style
│   └── Multiple MAs
└── Visual Aid: MA crossover examples
```

**Exercise 7.2**: Set up a moving average trading system:
1. Add 9 EMA, 21 EMA, and 50 SMA to daily chart
2. Identify current trend based on MA alignment
3. Find recent crossover signals
4. Set alerts for future crossovers

### Lesson 7.3: Oscillators
```
CONTENT REQUIREMENTS:
├── Relative Strength Index (RSI)
│   ├── Calculation
│   ├── Standard settings (14 period)
│   ├── Overbought/oversold (70/30)
│   ├── Divergence signals
│   ├── RSI trend lines
│   └── TWS configuration
├── MACD
│   ├── Components (MACD line, signal, histogram)
│   ├── Standard settings (12, 26, 9)
│   ├── Signal interpretation
│   ├── Histogram analysis
│   ├── Divergence
│   └── TWS configuration
├── Stochastic Oscillator
│   ├── %K and %D lines
│   ├── Fast vs Slow Stochastic
│   ├── Overbought/oversold
│   ├── Crossover signals
│   └── TWS configuration
├── Commodity Channel Index (CCI)
│   ├── Calculation
│   ├── Interpretation
│   ├── Trend following
│   └── TWS configuration
├── Williams %R
│   ├── Calculation
│   ├── vs Stochastic
│   └── Usage
├── Rate of Change (ROC)
│   ├── Momentum measurement
│   └── Configuration
└── Visual Aid: Oscillator panel setup
```

**Exercise 7.3**: Create an oscillator analysis setup:
1. Add RSI (14), MACD (12,26,9), and Stochastic (14,3,3)
2. Identify current readings for a selected stock
3. Look for divergences between price and oscillators
4. Document buy/sell signals from each indicator

### Lesson 7.4: Volatility Indicators
```
CONTENT REQUIREMENTS:
├── Bollinger Bands
│   ├── Calculation (20,2 standard)
│   ├── Band interpretation
│   ├── Squeeze identification
│   ├── Band riding
│   ├── Reversal signals
│   └── TWS configuration
├── Average True Range (ATR)
│   ├── Calculation
│   ├── Volatility measurement
│   ├── Position sizing use
│   ├── Stop loss placement
│   └── TWS configuration
├── Keltner Channels
│   ├── Calculation
│   ├── vs Bollinger Bands
│   ├── Squeeze combination
│   └── Configuration
├── Standard Deviation
│   ├── Statistical volatility
│   ├── Channel creation
│   └── Use cases
├── Donchian Channels
│   ├── Highest high/lowest low
│   ├── Breakout trading
│   └── Configuration
├── Volatility Stop
│   ├── Calculation
│   ├── Trailing method
│   └── Configuration
└── Visual Aid: Volatility indicator comparison
```

**Exercise 7.4**: Set up volatility analysis:
1. Add Bollinger Bands (20,2) and Keltner Channels (20,1.5)
2. Identify "squeeze" conditions (Bollinger inside Keltner)
3. Use ATR to calculate position size for $500 risk
4. Set volatility-based stop loss using 2x ATR

### Lesson 7.5: Volume Indicators
```
CONTENT REQUIREMENTS:
├── Volume Bars
│   ├── Standard volume display
│   ├── Color coding (up/down)
│   ├── Volume average overlay
│   └── Configuration
├── Volume Moving Average
│   ├── Calculation
│   ├── Relative volume
│   └── Configuration
├── On-Balance Volume (OBV)
│   ├── Calculation
│   ├── Trend confirmation
│   ├── Divergence signals
│   └── Configuration
├── Volume Profile
│   ├── Concept (price at volume)
│   ├── Point of Control (POC)
│   ├── Value Area
│   ├── Support/resistance from volume
│   └── Configuration
├── Accumulation/Distribution
│   ├── Calculation
│   ├── Money flow interpretation
│   └── Configuration
├── Money Flow Index (MFI)
│   ├── Volume-weighted RSI
│   ├── Interpretation
│   └── Configuration
├── VWAP (Volume-Weighted Average Price)
│   ├── Calculation
│   ├── Institutional benchmark
│   ├── Trading strategies
│   └── Configuration
└── Visual Aid: Volume analysis setup
```

**Exercise 7.5**: Create volume analysis workspace:
1. Add volume bars with 20-day average
2. Add OBV indicator
3. Add VWAP for intraday chart
4. Identify volume-confirmed price moves

### Lesson 7.6: Drawing Tools
```
CONTENT REQUIREMENTS:
├── Trend Lines
│   ├── Drawing technique
│   ├── Anchor points selection
│   ├── Trend line rules
│   ├── Extension settings
│   └── Alerts on trend line
├── Horizontal Lines
│   ├── Support levels
│   ├── Resistance levels
│   ├── Psychological levels
│   └── Previous high/low
├── Channels
│   ├── Parallel channel drawing
│   ├── Regression channel
│   ├── Standard deviation channel
│   └── Trading within channels
├── Fibonacci Tools
│   ├── Fibonacci Retracement
│   │   ├── Key levels (23.6, 38.2, 50, 61.8, 78.6)
│   │   ├── Drawing method
│   │   └── Trading application
│   ├── Fibonacci Extension
│   │   ├── Target levels
│   │   └── Drawing method
│   └── Fibonacci Time Zones
├── Gann Tools
│   ├── Gann Fan
│   ├── Gann Grid
│   └── Gann Square
├── Shapes and Annotations
│   ├── Rectangles (zones)
│   ├── Ellipses
│   ├── Text labels
│   ├── Price labels
│   └── Arrows
├── Measurement Tools
│   ├── Price measurement
│   ├── Bar count
│   ├── Percentage change
│   └── Time duration
├── Saving Drawings
│   ├── Symbol-specific
│   ├── Template inclusion
│   └── Sharing drawings
└── Visual Aid: Technical analysis chart with all tools
```

**Exercise 7.6**: Complete a full technical analysis:
1. Draw primary trend lines (support and resistance)
2. Identify key horizontal levels
3. Apply Fibonacci retracement to recent swing
4. Mark potential reversal zone
5. Save analysis with template

### Lesson 7.7: Chart Trading
```
CONTENT REQUIREMENTS:
├── Enabling Chart Trading
│   ├── Chart trader activation
│   ├── Button bar options
│   └── Default settings
├── Order Entry from Chart
│   ├── Buy button placement
│   ├── Sell button placement
│   ├── Click-to-trade options
│   ├── Limit order at click point
│   └── Market order buttons
├── Order Visualization
│   ├── Working orders on chart
│   ├── Order line colors
│   ├── Stop and target display
│   └── Position indicator
├── Order Modification
│   ├── Drag to change price
│   ├── Right-click modifications
│   ├── Cancel orders
│   └── Bracket visualization
├── Chart Trading Setup
│   ├── Recommended configuration
│   ├── Hotkey integration
│   ├── One-click trading settings
│   └── Safety settings
└── Visual Aid: Chart trading interface demonstration
```

**Exercise 7.7**: Trade directly from chart:
1. Enable chart trading
2. Place buy order by clicking on chart
3. Attach bracket orders (visible on chart)
4. Modify stop loss by dragging
5. Close position from chart

### Module 7 Assessment
```
QUIZ (40 questions):
├── Chart type selection scenarios
├── Indicator interpretation
├── Drawing tool application
├── Signal identification
└── Chart trading procedures

PRACTICAL TEST:
├── Set up complete multi-timeframe chart layout
├── Apply and interpret 10 indicators
├── Perform full technical analysis with drawings
├── Execute 5 trades from chart
├── Create analysis template
└── Time limit: 60 minutes
```

---

## MODULE 8: Market Scanner Mastery

### Learning Objectives
- Use and customize pre-built market scanners
- Create advanced custom scanners
- Integrate scanner results into trading workflow
- Build automated scanning systems

### Lesson 8.1: Scanner Fundamentals
```
CONTENT REQUIREMENTS:
├── What Scanners Do
│   ├── Real-time market filtering
│   ├── Universe of securities
│   ├── Criteria-based selection
│   └── Continuous updating
├── Accessing Market Scanner
│   ├── From menu
│   ├── From Mosaic
│   ├── Dedicated scanner window
│   └── Multiple scanner instances
├── Scanner Architecture
│   ├── Scan instrument type
│   ├── Scan parameter
│   ├── Filter criteria
│   └── Result display
├── Scanner Types
│   ├── Stock scanners
│   ├── Option scanners
│   ├── Futures scanners
│   ├── Forex scanners
│   └── Multi-asset scanners
└── Visual Aid: Scanner interface overview
```

**Exercise 8.1**: Open Market Scanner and explore 5 different pre-built scans. Document what each finds and how the results update.

### Lesson 8.2: Pre-Built Scanners
```
CONTENT REQUIREMENTS:
├── Top Gainers
│   ├── What it scans for
│   ├── Parameter options
│   ├── Use cases
│   └── Trading implications
├── Top Losers
│   ├── Short selling opportunities
│   ├── Oversold bounces
│   └── Use cases
├── Most Active by Volume
│   ├── Liquidity focus
│   ├── Momentum indication
│   └── Day trading application
├── Hot by Price (High/Low)
│   ├── New highs scanner
│   ├── New lows scanner
│   └── Breakout trading
├── High Dividend Yield
│   ├── Income investing
│   ├── Yield threshold
│   └── Ex-dividend considerations
├── Top Options Volume
│   ├── Unusual activity
│   ├── Trading implications
│   └── Configuration
├── Most Active Futures
│   ├── Futures market focus
│   └── Contract selection
├── Hot Contracts
│   ├── Volume spikes
│   └── Momentum plays
└── Visual Aid: Pre-built scanner gallery
```

**Exercise 8.2**: Use pre-built scanners to find:
1. Top 5 gainers > 5% today
2. Most active stocks by volume in tech sector
3. Stocks hitting 52-week highs
4. Highest options volume (unusual activity)

### Lesson 8.3: Custom Scanner Creation
```
CONTENT REQUIREMENTS:
├── Starting a Custom Scan
│   ├── New scan creation
│   ├── Naming convention
│   └── Save location
├── Instrument Selection
│   ├── Stock/ETF selection
│   ├── Exchange filters
│   ├── Index components
│   ├── Sector/Industry filters
│   └── Custom universe (watchlist)
├── Parameter Selection (COMPREHENSIVE)
│   ├── Price Parameters
│   │   ├── Last price range
│   │   ├── % change
│   │   ├── $ change
│   │   ├── Gap % open
│   │   └── Price vs MA
│   ├── Volume Parameters
│   │   ├── Today's volume
│   │   ├── Relative volume
│   │   ├── Average volume
│   │   └── Volume rate
│   ├── Technical Parameters
│   │   ├── RSI values
│   │   ├── MACD signals
│   │   ├── Moving average crossovers
│   │   └── Bollinger Band position
│   ├── Fundamental Parameters
│   │   ├── P/E ratio
│   │   ├── Market cap
│   │   ├── Revenue growth
│   │   └── Earnings date
│   ├── Options Parameters
│   │   ├── Implied volatility
│   │   ├── IV percentile
│   │   ├── Option volume
│   │   └── Put/call ratio
│   └── Custom Formulas
├── Filter Combination
│   ├── AND logic
│   ├── OR logic
│   ├── NOT logic
│   └── Complex combinations
├── Sort Options
│   ├── Primary sort
│   ├── Secondary sort
│   └── Ascending/descending
└── Visual Aid: Custom scanner builder walkthrough
```

**Exercise 8.3**: Build custom scanners:
1. Momentum Scanner: Price > 200 SMA, RSI > 50, Volume > 1.5x average
2. Mean Reversion: RSI < 30, Price near Bollinger lower band
3. Options Play: IV Rank > 50%, Earnings within 30 days
4. Save all scanners

### Lesson 8.4: Advanced Scanner Techniques
```
CONTENT REQUIREMENTS:
├── Multi-Criteria Strategies
│   ├── Combining technical + fundamental
│   ├── Cross-asset scanning
│   ├── Correlation-based scans
│   └── Complex logical structures
├── Time-Based Scanning
│   ├── Pre-market scanners
│   ├── Opening range scanners
│   ├── End of day scanners
│   └── Time-of-day filters
├── Relative Scanning
│   ├── Sector relative strength
│   ├── vs Index performance
│   ├── vs Historical norms
│   └── Peer comparison
├── Scanner Alerts
│   ├── New result notification
│   ├── Sound alerts
│   ├── Popup alerts
│   └── Mobile notifications
├── Scanner to Action
│   ├── Trading from scanner
│   ├── Adding to watchlist
│   ├── Chart link
│   └── Order entry from scanner
└── Visual Aid: Advanced scanner examples
```

**Exercise 8.4**: Create advanced scanner workflow:
1. Pre-market gap scanner (> 3% gap with volume)
2. Set up alert for new results
3. Link scanner to chart
4. Practice rapid analysis of scanner results

### Lesson 8.5: Scanner Optimization
```
CONTENT REQUIREMENTS:
├── Performance Considerations
│   ├── Scan universe size
│   ├── Number of criteria
│   ├── Refresh rate
│   └── Resource usage
├── Scan Quality Improvement
│   ├── Reducing false positives
│   ├── Confirmation filters
│   ├── Backtesting scan criteria
│   └── Iterative refinement
├── Scanner Templates
│   ├── Creating templates
│   ├── Sharing templates
│   ├── Template library
│   └── Quick template switching
├── Multiple Scanner Management
│   ├── Scanner dashboard
│   ├── Tabbed scanners
│   ├── Prioritizing results
│   └── Avoiding information overload
└── Visual Aid: Scanner optimization checklist
```

**Exercise 8.5**: Optimize your scanners:
1. Review scan from 8.3, reduce false positives
2. Add confirmation criteria
3. Create scanner template
4. Set up multi-scanner dashboard

### Module 8 Assessment
```
QUIZ (25 questions):
├── Scanner parameter knowledge
├── Filter logic
├── Use case scenarios
├── Optimization techniques
└── Alert configuration

PRACTICAL TEST:
├── Create 5 custom scanners from descriptions
├── Configure scanner alerts
├── Build scanner → chart → trade workflow
├── Optimize scanner for performance
└── Time limit: 35 minutes
```

---

## MODULE 9: Risk Navigator and Risk Management

### Learning Objectives
- Navigate and interpret Risk Navigator
- Perform portfolio stress testing
- Conduct what-if scenario analysis
- Implement systematic risk management

### Lesson 9.1: Risk Navigator Overview
```
CONTENT REQUIREMENTS:
├── Accessing Risk Navigator
│   ├── From menu
│   ├── Permissions required
│   └── Data requirements
├── Interface Layout
│   ├── Report selector
│   ├── Position summary
│   ├── Risk metrics panel
│   └── Scenario controls
├── Report Types
│   ├── Portfolio Risk
│   ├── P&L by Underlying
│   ├── Greeks Summary
│   ├── Stress Test
│   └── VAR Report
├── Position Display
│   ├── Grouping options
│   ├── Aggregation levels
│   ├── Position details
│   └── Hypothetical positions
└── Visual Aid: Risk Navigator interface tour
```

**Exercise 9.1**: Open Risk Navigator and:
1. View current portfolio risk
2. Navigate between report types
3. Identify total delta, gamma, theta exposure
4. Find largest risk concentration

### Lesson 9.2: Portfolio Greeks Analysis
```
CONTENT REQUIREMENTS:
├── Aggregate Delta
│   ├── Net portfolio delta
│   ├── Delta by underlying
│   ├── Dollar delta
│   └── Beta-weighted delta
├── Aggregate Gamma
│   ├── Total gamma exposure
│   ├── Gamma risk
│   └── Position-level gamma
├── Aggregate Theta
│   ├── Daily time decay
│   ├── Theta by expiration
│   └── Net theta position
├── Aggregate Vega
│   ├── Volatility exposure
│   ├── Vega by underlying
│   └── Vol sensitivity
├── Greeks Visualization
│   ├── Charts and graphs
│   ├── Risk distribution
│   └── Position contribution
├── Using Greeks for Risk Management
│   ├── Neutral positioning
│   ├── Hedging with Greeks
│   └── Position sizing from Greeks
└── Visual Aid: Greeks dashboard screenshot
```

**Exercise 9.2**: Analyze your option portfolio:
1. Calculate total portfolio delta
2. Identify theta decay per day
3. Find vega exposure
4. Plan adjustment to reduce delta by 50%

### Lesson 9.3: Stress Testing
```
CONTENT REQUIREMENTS:
├── Pre-built Stress Scenarios
│   ├── Market crash (-20%)
│   ├── Market rally (+20%)
│   ├── Volatility spike
│   ├── Interest rate change
│   └── Historical scenarios
├── Custom Stress Scenarios
│   ├── Price change scenario
│   ├── Volatility change scenario
│   ├── Time passage scenario
│   ├── Combined scenarios
│   └── Saving custom scenarios
├── Interpreting Stress Results
│   ├── P&L impact
│   ├── Margin impact
│   ├── Position-level impact
│   └── Risk concentration
├── Extreme Move Analysis
│   ├── Tail risk
│   ├── Black swan scenarios
│   └── Maximum drawdown
├── Scenario Reporting
│   ├── Report generation
│   ├── Export options
│   └── Comparison across scenarios
└── Visual Aid: Stress test results interpretation
```

**Exercise 9.3**: Conduct stress testing:
1. Run market crash (-15%) scenario
2. Run volatility spike (+50% IV) scenario
3. Create custom scenario (SPY -10%, QQQ -15%)
4. Document impact on portfolio P&L and margin

### Lesson 9.4: What-If Analysis
```
CONTENT REQUIREMENTS:
├── Hypothetical Positions
│   ├── Adding hypothetical trades
│   ├── Modifying existing positions
│   ├── Removing positions
│   └── Temporary analysis
├── What-If Scenarios
│   ├── "What if I buy X?"
│   ├── "What if I close Y?"
│   ├── "What if I hedge with Z?"
│   └── Position comparison
├── Impact Analysis
│   ├── Greeks change
│   ├── Risk change
│   ├── Margin impact
│   └── P&L scenarios
├── Hedge Analysis
│   ├── Finding optimal hedge
│   ├── Hedge ratio calculation
│   ├── Hedge cost vs benefit
│   └── Hedge effectiveness
├── From What-If to Order
│   ├── Converting to real order
│   ├── Order entry from Risk Navigator
│   └── Implementation workflow
└── Visual Aid: What-if analysis walkthrough
```

**Exercise 9.4**: Perform what-if analysis:
1. Add hypothetical position (100 shares SPY)
2. Analyze Greeks impact
3. Add hedge (protective put)
4. Compare risk with and without hedge
5. Convert hedge to real order

### Lesson 9.5: Value at Risk (VaR)
```
CONTENT REQUIREMENTS:
├── VaR Concepts
│   ├── What VaR measures
│   ├── Confidence levels (95%, 99%)
│   ├── Time horizon
│   └── VaR interpretation
├── VaR in Risk Navigator
│   ├── VaR report access
│   ├── VaR calculation method
│   ├── Reading VaR results
│   └── VaR by position
├── VaR Limitations
│   ├── Assumptions
│   ├── Tail risk underestimation
│   └── Correlation assumptions
├── Using VaR for Position Sizing
│   ├── VaR-based limits
│   ├── Capital allocation
│   └── Risk budgeting
├── Expected Shortfall (CVaR)
│   ├── Beyond VaR
│   ├── Tail risk measure
│   └── Interpretation
└── Visual Aid: VaR report explanation
```

**Exercise 9.5**: Work with VaR:
1. Generate VaR report for portfolio
2. Interpret 95% and 99% VaR values
3. Identify positions contributing most to VaR
4. Adjust position to reduce VaR by 20%

### Lesson 9.6: Margin Analysis
```
CONTENT REQUIREMENTS:
├── Margin Requirements Display
│   ├── Initial margin
│   ├── Maintenance margin
│   ├── Margin excess/deficit
│   └── Margin by position
├── Margin Impact Analysis
│   ├── New position margin
│   ├── Margin release on close
│   ├── Worst-case margin
│   └── Margin stress scenarios
├── Margin Models
│   ├── Reg T margin
│   ├── Portfolio margin
│   ├── Model comparison
│   └── Margin optimization
├── Margin Alerts and Monitoring
│   ├── Setting margin alerts
│   ├── Margin utilization
│   ├── Pre-trade margin check
│   └── Margin call handling
└── Visual Aid: Margin analysis interface
```

**Exercise 9.6**: Margin analysis:
1. View current margin utilization
2. Analyze margin impact of adding new position
3. Set alert at 80% margin utilization
4. Create margin stress scenario

### Module 9 Assessment
```
QUIZ (30 questions):
├── Greeks interpretation
├── Stress testing scenarios
├── VaR concepts
├── What-if analysis
└── Margin management

PRACTICAL TEST:
├── Navigate Risk Navigator efficiently
├── Conduct 3 stress test scenarios
├── Perform what-if analysis for hedge
├── Calculate and interpret VaR
├── Create risk report
└── Time limit: 40 minutes
```

---

## MODULE 10: Volatility Lab and Analytics

### Learning Objectives
- Analyze implied volatility across dimensions
- Understand volatility term structure and skew
- Use Probability Lab for trade planning
- Apply volatility analysis to trading decisions

### Lesson 10.1: Volatility Lab Overview
```
CONTENT REQUIREMENTS:
├── Accessing Volatility Lab
│   ├── From menu
│   ├── Symbol selection
│   └── Data requirements
├── Interface Components
│   ├── IV chart
│   ├── HV chart
│   ├── Term structure
│   ├── Skew display
│   └── Statistics panel
├── Key Metrics
│   ├── Current IV
│   ├── IV Rank
│   ├── IV Percentile
│   ├── Historical volatility
│   └── HV-IV spread
├── Time Frames
│   ├── Daily view
│   ├── Intraday view
│   ├── Historical range
│   └── Custom periods
└── Visual Aid: Volatility Lab interface tour
```

**Exercise 10.1**: Open Volatility Lab for a selected stock:
1. Record current IV and IV Rank
2. Compare to 52-week IV range
3. Note HV-IV relationship
4. Identify if IV is high or low relative to history

### Lesson 10.2: Implied Volatility Analysis
```
CONTENT REQUIREMENTS:
├── IV Calculation
│   ├── How IV is derived
│   ├── Model assumptions
│   └── IV sources in TWS
├── IV Interpretation
│   ├── High IV implications
│   ├── Low IV implications
│   ├── IV as fear gauge
│   └── IV mean reversion
├── IV Rank vs IV Percentile
│   ├── IV Rank calculation
│   ├── IV Percentile calculation
│   ├── When to use each
│   └── Trading rules based on each
├── IV Surface
│   ├── Strike dimension
│   ├── Expiration dimension
│   ├── Surface visualization
│   └── Anomaly identification
├── IV Changes Analysis
│   ├── IV expansion events
│   ├── IV crush (post-earnings)
│   ├── Predicting IV moves
│   └── IV-based signals
└── Visual Aid: IV analysis charts
```

**Exercise 10.2**: Conduct IV analysis:
1. Find 3 stocks with IV Rank > 80%
2. Find 3 stocks with IV Rank < 20%
3. Analyze one stock approaching earnings (IV expansion)
4. Document trading strategy based on IV levels

### Lesson 10.3: Historical Volatility Analysis
```
CONTENT REQUIREMENTS:
├── HV Calculation Methods
│   ├── Close-to-close
│   ├── Parkinson (high-low)
│   ├── Garman-Klass
│   └── Yang-Zhang
├── HV Time Periods
│   ├── 10-day HV
│   ├── 20-day HV
│   ├── 30-day HV
│   ├── 60-day HV
│   └── Annualization
├── HV vs IV Comparison
│   ├── HV-IV spread interpretation
│   ├── IV premium/discount
│   ├── Mean reversion tendencies
│   └── Trading implications
├── Realized vs Implied
│   ├── Tracking accuracy
│   ├── Volatility risk premium
│   └── Strategy implications
├── HV Forecasting
│   ├── Volatility clustering
│   ├── GARCH concepts
│   └── Regime changes
└── Visual Aid: HV vs IV comparison charts
```

**Exercise 10.3**: Historical volatility analysis:
1. Calculate HV-IV spread for selected stock
2. Determine if options are "cheap" or "expensive"
3. Identify volatility regime (high/low/normal)
4. Recommend strategy based on HV-IV relationship

### Lesson 10.4: Term Structure Analysis
```
CONTENT REQUIREMENTS:
├── Term Structure Concept
│   ├── IV across expirations
│   ├── Normal vs inverted structure
│   ├── Contango vs backwardation
│   └── Causes of term structure shapes
├── Term Structure in TWS
│   ├── Display options
│   ├── Expiration selection
│   ├── ATM vs other strikes
│   └── Custom views
├── Trading Term Structure
│   ├── Calendar spread opportunities
│   ├── Front month vs back month
│   ├── Roll timing
│   └── Event-driven structure
├── Term Structure Patterns
│   ├── Earnings effect
│   ├── Macro event effect
│   ├── Typical patterns
│   └── Anomaly detection
└── Visual Aid: Term structure charts
```

**Exercise 10.4**: Analyze term structure:
1. Display term structure for selected stock
2. Identify shape (normal, flat, inverted)
3. Find earnings impact on term structure
4. Identify calendar spread opportunity

### Lesson 10.5: Volatility Skew
```
CONTENT REQUIREMENTS:
├── Skew Concept
│   ├── IV variation by strike
│   ├── Put skew (typical equity pattern)
│   ├── Call skew
│   ├── Smile pattern
│   └── Historical context
├── Skew in TWS
│   ├── Skew chart display
│   ├── Single expiration view
│   ├── Multi-expiration comparison
│   └── Skew metrics
├── Interpreting Skew
│   ├── Fear premium in puts
│   ├── Demand patterns
│   ├── Hedging activity signals
│   └── Skew richness/cheapness
├── Trading Skew
│   ├── Skew trades (risk reversals)
│   ├── Vertical spread selection
│   ├── Put vs call spread pricing
│   └── Skew mean reversion
├── Skew Changes
│   ├── Pre-earnings skew
│   ├── Market stress impact
│   └── Event-driven changes
└── Visual Aid: Skew patterns and interpretation
```

**Exercise 10.5**: Analyze volatility skew:
1. Display skew for near-term expiration
2. Compare OTM put IV to OTM call IV
3. Identify skew steepness
4. Find risk reversal trade opportunity

### Lesson 10.6: Probability Lab
```
CONTENT REQUIREMENTS:
├── Probability Lab Access
│   ├── From menu
│   ├── Symbol selection
│   └── Interface overview
├── Probability Distribution
│   ├── What distribution shows
│   ├── Reading probability curve
│   ├── Standard deviations
│   └── Probability at price levels
├── Expected Move
│   ├── Calculation
│   ├── By expiration
│   ├── Trading range estimation
│   └── Confidence intervals
├── Strategy Analysis
│   ├── Probability of profit
│   ├── Expected value
│   ├── Risk/reward visualization
│   └── Breakeven probabilities
├── Custom Scenario Analysis
│   ├── Setting target prices
│   ├── Probability of reaching target
│   ├── Multiple targets
│   └── Time-based probability
├── Integration with Trading
│   ├── Strike selection based on probability
│   ├── Position sizing
│   ├── Trade planning
│   └── Exit planning
└── Visual Aid: Probability Lab walkthrough
```

**Exercise 10.6**: Use Probability Lab:
1. View probability distribution for stock
2. Determine expected move for nearest expiration
3. Find probability of stock being above/below current price
4. Select strike with >70% probability of expiring OTM
5. Analyze iron condor probability of profit

### Module 10 Assessment
```
QUIZ (30 questions):
├── IV concepts and interpretation
├── HV-IV relationship
├── Term structure analysis
├── Skew interpretation
└── Probability concepts

PRACTICAL TEST:
├── Complete volatility analysis for 3 stocks
├── Identify term structure anomalies
├── Analyze skew and recommend trade
├── Use Probability Lab for trade planning
├── Create volatility-based trading thesis
└── Time limit: 45 minutes
```

---

## MODULE 11: API and Automation

### Learning Objectives
- Configure TWS API for external connections
- Use Excel DDE/RTD for data retrieval
- Understand algorithmic trading possibilities
- Implement basic automation workflows

### Lesson 11.1: API Configuration
```
CONTENT REQUIREMENTS:
├── API Overview
│   ├── What TWS API enables
│   ├── Available APIs (Python, Java, C++, etc.)
│   ├── API vs FIX CTCI
│   └── Use cases
├── Enabling API in TWS
│   ├── Configuration menu navigation
│   ├── Enable ActiveX and Socket Clients
│   ├── Socket port settings
│   ├── Trusted IP addresses
│   └── Master Client ID
├── API Settings
│   ├── Read-only API option
│   ├── Allow connections from localhost
│   ├── Logging settings
│   ├── Pre-caution settings
│   └── Order confirmation settings
├── Security Considerations
│   ├── Network security
│   ├── IP restrictions
│   ├── Port security
│   └── Best practices
├── Testing Connection
│   ├── Connection verification
│   ├── Sample applications
│   └── Troubleshooting
└── Visual Aid: API configuration walkthrough
```

**Exercise 11.1**: Configure TWS for API access:
1. Enable socket client connections
2. Set port to 7497 (paper) or 7496 (live)
3. Add localhost to trusted IPs
4. Test connection status

### Lesson 11.2: Excel Integration (DDE/RTD)
```
CONTENT REQUIREMENTS:
├── DDE Basics
│   ├── What is DDE
│   ├── DDE formula syntax
│   ├── Real-time data retrieval
│   └── Limitations
├── RTD Functions
│   ├── RTD formula structure
│   ├── Available data points
│   ├── Throttling settings
│   └── Error handling
├── Market Data in Excel
│   ├── Getting quotes
│   ├── Position data
│   ├── Account data
│   ├── Historical data
│   └── Option chains
├── Order Entry from Excel
│   ├── Order formulas
│   ├── Order status
│   ├── Modify and cancel
│   └── Bracket orders
├── Building Trading Spreadsheets
│   ├── Dashboard design
│   ├── Calculation integration
│   ├── Alert mechanisms
│   └── Sample templates
└── Visual Aid: Excel integration examples
```

**Exercise 11.2**: Build Excel integration:
1. Create spreadsheet with real-time quotes (5 symbols)
2. Add position data display
3. Create order entry cell
4. Build simple P&L calculator

### Lesson 11.3: IBot (AI Assistant)
```
CONTENT REQUIREMENTS:
├── IBot Overview
│   ├── What IBot does
│   ├── Accessing IBot
│   └── Voice vs text
├── Market Data Commands
│   ├── Quote retrieval
│   ├── Chart requests
│   ├── Option chain access
│   └── News queries
├── Trading Commands
│   ├── Order placement
│   ├── Order modification
│   ├── Position queries
│   └── Account inquiries
├── Analysis Commands
│   ├── Technical analysis
│   ├── Fundamental queries
│   ├── Comparison requests
│   └── Screening
├── Best Practices
│   ├── Command syntax
│   ├── Confirmation handling
│   ├── Error recovery
│   └── Efficiency tips
└── Visual Aid: IBot command examples
```

**Exercise 11.3**: Use IBot for:
1. Get quote for AAPL
2. Show AAPL daily chart
3. Buy 10 shares AAPL at market (paper trading)
4. What's my position in AAPL?

### Lesson 11.4: Automation Concepts
```
CONTENT REQUIREMENTS:
├── Automation Levels
│   ├── Manual with assistance
│   ├── Semi-automated
│   ├── Fully automated
│   └── Appropriate use cases
├── Automation Methods
│   ├── Conditional orders (built-in)
│   ├── Scanner-triggered
│   ├── Alert-based
│   ├── API-driven
│   └── Third-party platforms
├── Building Automated Workflows
│   ├── Strategy definition
│   ├── Entry rules
│   ├── Exit rules
│   ├── Risk management rules
│   └── Implementation options
├── Risk Management for Automation
│   ├── Position limits
│   ├── Loss limits
│   ├── Manual override
│   └── Monitoring requirements
├── Compliance Considerations
│   ├── Pattern day trader rules
│   ├── Regulatory requirements
│   └── Documentation
└── Visual Aid: Automation workflow diagrams
```

**Exercise 11.4**: Design automation workflow:
1. Define simple moving average crossover strategy
2. Determine entry/exit rules
3. Set risk management parameters
4. Choose implementation method
5. Document monitoring plan

### Module 11 Assessment
```
QUIZ (20 questions):
├── API configuration
├── Excel integration
├── IBot commands
├── Automation concepts
└── Risk management for automation

PRACTICAL TEST:
├── Configure TWS API correctly
├── Build Excel data retrieval sheet
├── Execute trades via IBot
├── Design automation workflow document
└── Time limit: 35 minutes
```

---

## MODULE 12: Professional Trading Setups

### Learning Objectives
- Design workspace layouts optimized for specific trading styles
- Configure hotkeys and shortcuts for rapid execution
- Implement professional-grade risk management
- Optimize TWS performance for demanding workflows

### Lesson 12.1: Day Trading Configuration
```
CONTENT REQUIREMENTS:
├── Workspace Design
│   ├── Multi-monitor layout
│   │   ├── Monitor 1: Execution (BookTrader)
│   │   ├── Monitor 2: Charts (multiple timeframes)
│   │   ├── Monitor 3: Scanners + Level II
│   │   └── Monitor 4: Portfolio + Risk
│   ├── Single monitor layout
│   └── Laptop configuration
├── BookTrader Optimization
│   ├── Price ladder settings
│   ├── One-click configuration
│   ├── Auto-center settings
│   └── Order display
├── Hotkey Setup (COMPREHENSIVE)
│   ├── Buy at market (F1)
│   ├── Sell at market (F2)
│   ├── Buy at bid (F3)
│   ├── Sell at ask (F4)
│   ├── Cancel all (F5)
│   ├── Flatten position (F6)
│   ├── Add to position (F7)
│   ├── Reduce position (F8)
│   ├── Bracket attach (F9)
│   └── Custom hotkeys
├── Order Defaults for Speed
│   ├── Default quantity
│   ├── Default order type
│   ├── Bracket defaults
│   └── Confirmation bypass
├── Real-time Data Setup
│   ├── Level II data
│   ├── Time and sales
│   ├── Required subscriptions
│   └── Latency optimization
├── Risk Management
│   ├── Daily loss limit
│   ├── Per-trade risk
│   ├── Position limits
│   └── Automatic stops
└── Visual Aid: Complete day trading setup screenshots
```

**Exercise 12.1**: Build day trading configuration:
1. Create multi-chart layout (1min, 5min, 15min, 60min)
2. Configure BookTrader with all hotkeys
3. Set up scanner for momentum stocks
4. Establish daily loss limit of $500
5. Practice 20 round-trip paper trades

### Lesson 12.2: Swing Trading Configuration
```
CONTENT REQUIREMENTS:
├── Workspace Design
│   ├── Research focus layout
│   ├── Watchlist organization
│   ├── Chart setup (daily focus)
│   └── Alert management
├── Watchlist Organization
│   ├── Sector-based lists
│   ├── Setup-based lists
│   ├── Earnings calendar integration
│   └── Column configuration
├── Chart Configuration
│   ├── Daily and weekly charts
│   ├── Indicator selection
│   ├── Drawing templates
│   └── Multi-timeframe analysis
├── Order Management
│   ├── GTC order usage
│   ├── Conditional orders
│   ├── Alert-to-order workflow
│   └── Bracket strategies
├── Scanner Setup
│   ├── End-of-day scans
│   ├── Breakout candidates
│   ├── Technical setup scans
│   └── Fundamental filters
├── Alert Configuration
│   ├── Price alerts
│   ├── Indicator alerts
│   ├── Scanner alerts
│   └── Mobile notifications
└── Visual Aid: Swing trading workspace
```

**Exercise 12.2**: Build swing trading configuration:
1. Create watchlist with 20 stocks in 4 sectors
2. Set up daily chart template with your indicators
3. Create end-of-day scanner
4. Configure 5 price alerts
5. Establish weekly review workflow

### Lesson 12.3: Options Trading Configuration
```
CONTENT REQUIREMENTS:
├── Workspace Design
│   ├── OptionTrader central
│   ├── Volatility Lab integration
│   ├── Risk Navigator visible
│   └── Multi-underlying monitoring
├── OptionTrader Optimization
│   ├── Chain configuration
│   ├── Greeks display
│   ├── Strategy templates
│   └── Quick strategy buttons
├── Volatility Analysis Setup
│   ├── IV Rank display
│   ├── Term structure view
│   ├── Skew analysis
│   └── HV comparison
├── Position Management
│   ├── Greeks monitoring
│   ├── Rolling workflow
│   ├── Adjustment alerts
│   └── Expiration management
├── Risk Navigator Setup
│   ├── Automatic refresh
│   ├── Key metric display
│   ├── Stress test templates
│   └── What-if quick access
├── Specialized Scanners
│   ├── High IV rank scanner
│   ├── Unusual options activity
│   ├── Earnings plays scanner
│   └── Dividend plays
└── Visual Aid: Options trading workspace
```

**Exercise 12.3**: Build options trading configuration:
1. Configure OptionTrader with all Greeks displayed
2. Set up Volatility Lab for 5 underlyings
3. Create options scanner (IV Rank > 50)
4. Configure Risk Navigator for portfolio Greeks
5. Build rolling order template

### Lesson 12.4: Long-Term Investing Configuration
```
CONTENT REQUIREMENTS:
├── Workspace Design
│   ├── Portfolio focus
│   ├── Research integration
│   ├── Performance tracking
│   └── Minimal noise layout
├── Portfolio Display
│   ├── Position overview
│   ├── Allocation visualization
│   ├── Performance metrics
│   └── Dividend tracking
├── Research Tools
│   ├── Fundamentals Explorer
│   ├── Analyst ratings
│   ├── Earnings calendar
│   └── News filtering
├── Rebalancing Setup
│   ├── Target allocation definition
│   ├── Rebalance alerts
│   ├── Tax-lot selection
│   └── Scheduled reviews
├── Income Features
│   ├── Dividend calendar
│   ├── Yield tracking
│   ├── DRIP configuration
│   └── Income projections
├── Reporting Setup
│   ├── PortfolioAnalyst access
│   ├── Performance benchmarks
│   ├── Tax reporting
│   └── Custom reports
└── Visual Aid: Investor workspace
```

**Exercise 12.4**: Build investor configuration:
1. Set up portfolio view with key metrics
2. Configure target allocation (60/40 stocks/bonds)
3. Enable dividend reinvestment
4. Create monthly rebalance review schedule
5. Generate performance report

### Lesson 12.5: Performance Optimization
```
CONTENT REQUIREMENTS:
├── TWS Performance Settings
│   ├── Memory allocation
│   ├── Java settings
│   ├── Update frequency
│   └── Data caching
├── Data Management
│   ├── Subscription optimization
│   ├── Snapshot vs streaming
│   ├── Symbol limit management
│   └── Page refresh settings
├── Network Optimization
│   ├── Connection settings
│   ├── Server selection
│   ├── Latency reduction
│   └── Reconnection settings
├── Display Optimization
│   ├── Animation settings
│   ├── Color depth
│   ├── Font rendering
│   └── Chart smoothing
├── Startup Optimization
│   ├── Default layout
│   ├── Pre-loaded pages
│   ├── Auto-start settings
│   └── Login optimization
└── Visual Aid: Performance settings checklist
```

**Exercise 12.5**: Optimize TWS performance:
1. Configure memory settings
2. Optimize data subscriptions
3. Set up efficient default layout
4. Test startup time
5. Document optimal settings

### Module 12 Assessment
```
QUIZ (25 questions):
├── Day trading setup requirements
├── Swing trading workflow
├── Options trading configuration
├── Investor setup
└── Performance optimization

PRACTICAL TEST:
├── Build complete day trading workspace
├── Configure options trading layout
├── Set up investor monitoring dashboard
├── Demonstrate hotkey proficiency
├── Complete performance optimization
└── Time limit: 60 minutes
```

---

## MODULE 13: Troubleshooting and Support

### Learning Objectives
- Diagnose and resolve common TWS issues
- Understand error messages and their solutions
- Navigate IBKR support resources
- Implement preventive maintenance

### Lesson 13.1: Connection Issues
```
CONTENT REQUIREMENTS:
├── Login Problems
│   ├── Invalid credentials
│   ├── Two-factor authentication issues
│   ├── Account locked
│   └── Session conflicts
├── Connection Drops
│   ├── Internet issues
│   ├── Server issues
│   ├── Firewall problems
│   └── ISP throttling
├── Server Selection
│   ├── Available servers
│   ├── Best server selection
│   ├── Manual override
│   └── Failover configuration
├── Firewall and Proxy
│   ├── Required ports
│   ├── Firewall configuration
│   ├── Proxy settings
│   └── VPN considerations
├── Reconnection Strategy
│   ├── Automatic reconnection
│   ├── Manual reconnection
│   ├── Order handling during disconnect
│   └── Position verification
└── Visual Aid: Connection troubleshooting flowchart
```

**Exercise 13.1**: Connection troubleshooting practice:
1. Document current connection settings
2. Identify server being used
3. Test alternative servers
4. Verify firewall settings
5. Create reconnection checklist

### Lesson 13.2: Market Data Issues
```
CONTENT REQUIREMENTS:
├── No Data Displayed
│   ├── Subscription verification
│   ├── Symbol entry issues
│   ├── Exchange selection
│   └── Permission problems
├── Delayed Data
│   ├── Delayed vs real-time
│   ├── Subscription upgrade
│   ├── Display verification
│   └── Time display issues
├── Missing Symbols
│   ├── Symbol lookup
│   ├── Exchange routing
│   ├── Contract details
│   └── Alternative symbols
├── Data Quality Issues
│   ├── Stale data
│   ├── Incorrect prices
│   ├── Missing history
│   └── Reporting issues
├── Subscription Management
│   ├── Viewing subscriptions
│   ├── Adding subscriptions
│   ├── Removing subscriptions
│   └── Cost management
└── Visual Aid: Market data troubleshooting guide
```

**Exercise 13.2**: Market data troubleshooting:
1. Verify current market data subscriptions
2. Test real-time vs delayed data
3. Find alternative symbol for international stock
4. Report data quality issue (practice)

### Lesson 13.3: Order Issues
```
CONTENT REQUIREMENTS:
├── Order Rejections
│   ├── Insufficient funds
│   ├── Position limits
│   ├── Invalid parameters
│   ├── Trading halts
│   └── Exchange rules
├── Margin Errors
│   ├── Initial margin insufficient
│   ├── Maintenance margin issues
│   ├── Margin call handling
│   └── Day trading margin
├── Trading Permission Errors
│   ├── Permission requirements
│   ├── Requesting permissions
│   ├── Complex options permission
│   └── Futures permissions
├── Order Status Issues
│   ├── Pending status stuck
│   ├── Partial fills
│   ├── Order not canceling
│   └── Phantom orders
├── Execution Issues
│   ├── Unexpected fills
│   ├── Price discrepancies
│   ├── Execution quality
│   └── Trade breaks
└── Visual Aid: Order error resolution flowchart
```

**Exercise 13.3**: Order troubleshooting:
1. Interpret 5 common rejection messages
2. Calculate margin requirement for sample trade
3. Check trading permissions
4. Practice order modification and cancellation

### Lesson 13.4: Performance Issues
```
CONTENT REQUIREMENTS:
├── Slow Performance
│   ├── System resource check
│   ├── TWS memory allocation
│   ├── Too many windows/pages
│   └── Data overload
├── Chart Performance
│   ├── Too many indicators
│   ├── Historical data loading
│   ├── Drawing tool impact
│   └── Chart optimization
├── Memory Issues
│   ├── Java heap space
│   ├── Memory leaks
│   ├── Garbage collection
│   └── Memory optimization
├── Crash Prevention
│   ├── Stable configuration
│   ├── Regular restarts
│   ├── Layout backup
│   └── Settings preservation
├── Diagnostic Tools
│   ├── Log file review
│   ├── Performance monitoring
│   ├── Resource usage
│   └── IBKR support tools
└── Visual Aid: Performance optimization checklist
```

**Exercise 13.4**: Performance optimization:
1. Check current memory usage
2. Identify resource-heavy components
3. Optimize configuration
4. Benchmark before/after performance

### Lesson 13.5: Getting Help
```
CONTENT REQUIREMENTS:
├── IBKR Knowledge Base
│   ├── Accessing knowledge base
│   ├── Search techniques
│   ├── Common articles
│   └── Video tutorials
├── Customer Service
│   ├── Contact methods
│   ├── Ticket submission
│   ├── Phone support
│   ├── Chat support
│   └── Response expectations
├── Community Resources
│   ├── IBKR forums
│   ├── Reddit communities
│   ├── Trading communities
│   └── Third-party resources
├── Problem Documentation
│   ├── Screenshot capture
│   ├── Log collection
│   ├── Error recording
│   └── Reproduction steps
├── Escalation Process
│   ├── When to escalate
│   ├── How to escalate
│   └── Regulatory options
└── Visual Aid: Support resource map
```

**Exercise 13.5**: Support practice:
1. Navigate IBKR Knowledge Base
2. Find article on specific topic
3. Document a mock issue with screenshots
4. Identify appropriate support channel

### Module 13 Assessment
```
QUIZ (20 questions):
├── Connection troubleshooting
├── Data issue resolution
├── Order error interpretation
├── Performance optimization
└── Support navigation

PRACTICAL TEST:
├── Diagnose simulated connection issue
├── Resolve market data problem
├── Interpret and fix order rejection
├── Optimize performance configuration
├── Submit support request (mock)
└── Time limit: 30 minutes
```

---

## MODULE 14: Capstone Projects

### Project 1: Complete Trading System Design
```
PROJECT REQUIREMENTS:
├── Objective
│   └── Design and implement complete trading system for specific strategy
├── Deliverables
│   ├── Strategy documentation
│   ├── Complete workspace layout
│   ├── Scanner configuration
│   ├── Risk management rules
│   ├── Order templates
│   └── Performance tracking setup
├── Requirements
│   ├── Define trading strategy (entry, exit, risk)
│   ├── Configure all necessary TWS tools
│   ├── Create appropriate scanners
│   ├── Set up risk management
│   ├── Document workflow
│   └── Execute 10 paper trades
├── Evaluation Criteria
│   ├── Strategy clarity and viability
│   ├── TWS configuration quality
│   ├── Risk management implementation
│   ├── Workflow efficiency
│   └── Documentation completeness
└── Time Allocation: 4 hours
```

### Project 2: Options Strategy Implementation
```
PROJECT REQUIREMENTS:
├── Objective
│   └── Implement complete options trading workflow
├── Deliverables
│   ├── Volatility analysis for 5 underlyings
│   ├── Strategy selection rationale
│   ├── Position sizing framework
│   ├── Entry execution
│   ├── Risk management plan
│   └── Exit/adjustment rules
├── Requirements
│   ├── Analyze IV rank across watchlist
│   ├── Select appropriate strategy based on analysis
│   ├── Execute multi-leg option trade
│   ├── Set up position monitoring
│   ├── Create adjustment scenarios
│   └── Document entire process
├── Evaluation Criteria
│   ├── Volatility analysis accuracy
│   ├── Strategy selection logic
│   ├── Execution quality
│   ├── Risk management
│   └── Adjustment planning
└── Time Allocation: 3 hours
```

### Project 3: Portfolio Management System
```
PROJECT REQUIREMENTS:
├── Objective
│   └── Build complete portfolio management workflow
├── Deliverables
│   ├── Portfolio construction plan
│   ├── Monitoring dashboard
│   ├── Rebalancing system
│   ├── Risk analysis setup
│   └── Reporting framework
├── Requirements
│   ├── Define investment policy
│   ├── Create diversified portfolio (10+ positions)
│   ├── Set up Risk Navigator monitoring
│   ├── Configure rebalancing alerts
│   ├── Generate performance report
│   └── Create stress test scenarios
├── Evaluation Criteria
│   ├── Portfolio construction quality
│   ├── Monitoring effectiveness
│   ├── Risk management implementation
│   ├── Rebalancing process
│   └── Reporting completeness
└── Time Allocation: 3 hours
```

### Project 4: Automation Workflow Design
```
PROJECT REQUIREMENTS:
├── Objective
│   └── Design semi-automated trading workflow
├── Deliverables
│   ├── Automation strategy document
│   ├── Scanner-based triggers
│   ├── Conditional order chains
│   ├── Alert system
│   └── Manual override procedures
├── Requirements
│   ├── Define automation goals
│   ├── Create scanner-triggered workflow
│   ├── Implement conditional order chains
│   ├── Set up monitoring alerts
│   ├── Document risk controls
│   └── Test in paper trading
├── Evaluation Criteria
│   ├── Automation logic soundness
│   ├── Implementation completeness
│   ├── Risk control adequacy
│   ├── Monitoring effectiveness
│   └── Documentation quality
└── Time Allocation: 4 hours
```

---

## Course Completion Requirements

### Certification Criteria
```
REQUIREMENTS FOR COURSE COMPLETION:
├── Module Completion
│   ├── All 13 modules completed
│   ├── All exercises finished
│   └── All assessments passed (>80%)
├── Practical Competency
│   ├── Complete all practical tests
│   ├── Minimum 70% on each test
│   └── Demonstrate tool proficiency
├── Capstone Projects
│   ├── Complete at least 2 of 4 projects
│   ├── Meet all project requirements
│   └── Pass project evaluation
└── Time Investment
    └── Estimated 40-60 hours total
```

### Skill Verification Matrix
```
COMPETENCY VERIFICATION:
├── Beginner Level (Modules 1-3)
│   ├── Navigate TWS confidently
│   ├── Execute basic orders
│   └── Manage simple positions
├── Intermediate Level (Modules 4-7)
│   ├── Use all order types appropriately
│   ├── Trade options effectively
│   ├── Perform technical analysis
│   └── Use scanners productively
├── Advanced Level (Modules 8-11)
│   ├── Manage portfolio risk
│   ├── Analyze volatility
│   ├── Use API features
│   └── Build automated workflows
└── Expert Level (Modules 12-14)
    ├── Design professional setups
    ├── Troubleshoot issues independently
    └── Implement complete trading systems
```

---

## Output Format

Generate course as structured collection of Markdown files:

```
docs/interactive-brokers-tws-course/
├── README.md (course overview and navigation)
├── syllabus.md (complete course syllabus)
├── module-01-foundations/
│   ├── README.md (module overview)
│   ├── lesson-01-intro.md
│   ├── lesson-02-setup.md
│   ├── lesson-03-interface.md
│   ├── lesson-04-navigation.md
│   ├── exercises.md
│   └── assessment.md
├── module-02-mosaic/
│   └── [lessons, exercises, assessment]
├── module-03-classic-tws/
│   └── [lessons, exercises, assessment]
├── module-04-order-types/
│   └── [lessons, exercises, assessment]
├── module-05-option-trader/
│   └── [lessons, exercises, assessment]
├── module-06-specialized-views/
│   └── [lessons, exercises, assessment]
├── module-07-charts/
│   └── [lessons, exercises, assessment]
├── module-08-scanners/
│   └── [lessons, exercises, assessment]
├── module-09-risk-management/
│   └── [lessons, exercises, assessment]
├── module-10-volatility/
│   └── [lessons, exercises, assessment]
├── module-11-api/
│   └── [lessons, exercises, assessment]
├── module-12-professional-setups/
│   └── [lessons, exercises, assessment]
├── module-13-troubleshooting/
│   └── [lessons, exercises, assessment]
├── module-14-capstone/
│   ├── project-01-trading-system.md
│   ├── project-02-options-strategy.md
│   ├── project-03-portfolio-management.md
│   └── project-04-automation.md
├── resources/
│   ├── keyboard-shortcuts.md
│   ├── glossary.md
│   ├── quick-reference.md
│   └── troubleshooting-guide.md
└── appendices/
    ├── exercise-solutions.md
    ├── assessment-answers.md
    └── additional-resources.md
```

---

## Execution Instructions

1. **Create Course Structure**: Set up directory structure and navigation
2. **Build Foundation Modules**: Complete Modules 1-3 with full detail
3. **Develop Core Modules**: Complete Modules 4-7
4. **Create Advanced Content**: Complete Modules 8-11
5. **Build Expert Content**: Complete Modules 12-14
6. **Develop Assessments**: Create all quizzes and practical tests
7. **Create Capstone Projects**: Full project specifications
8. **Add Resources**: Quick references, glossary, solutions
9. **Review and Polish**: Cross-reference, consistency check

Begin by creating the course syllabus and module structure, then systematically develop each module from beginner through expert level.
