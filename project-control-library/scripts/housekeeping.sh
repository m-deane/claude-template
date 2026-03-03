#!/usr/bin/env bash
# Housekeeping — Directory cleanup automation for managed projects.
#
# Usage:
#   bash housekeeping.sh ~/projects/my-project       # Clean specific project
#   bash housekeeping.sh --all                        # Clean all managed projects
#   bash housekeeping.sh --dry-run ~/projects/proj    # Preview changes only
#
# Actions:
#   - Move misplaced files from root to correct directories
#   - Delete stale temp files (.tmp, .bak, .log > 7 days)
#   - Remove .DS_Store files
#   - Create standard directories if missing
#   - Report what was moved/deleted

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_PATH="$SCRIPT_DIR/../config.json"
DRY_RUN=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_action() { echo -e "${GREEN}[ACTION]${NC} $1"; }
log_dry() { echo -e "${YELLOW}[DRY RUN]${NC} Would: $1"; }

# Files allowed in project root
ALLOWED_ROOT_FILES=(
    "CLAUDE.md" "README.md" "STATUS.md" "LICENSE" "LICENSE.md"
    "package.json" "package-lock.json" "yarn.lock" "pnpm-lock.yaml"
    "tsconfig.json" "tsconfig.*.json" "next.config.ts" "next.config.js" "next.config.mjs"
    "vitest.config.ts" "vitest.config.js" "jest.config.ts" "jest.config.js"
    "tailwind.config.ts" "tailwind.config.js" "postcss.config.mjs" "postcss.config.js"
    ".gitignore" ".eslintrc.json" ".eslintrc.js" ".prettierrc" ".prettierrc.json"
    ".env.example" ".env.local" ".env"
    "Dockerfile" "docker-compose.yml" "docker-compose.yaml"
    "Makefile" "Taskfile.yml"
    "requirements.txt" "pyproject.toml" "setup.py" "setup.cfg"
    "go.mod" "go.sum" "Cargo.toml" "Cargo.lock"
    "components.json" "middleware.ts" "middleware.js"
)

# Directories allowed in project root
ALLOWED_ROOT_DIRS=(
    "src" "app" "lib" "tests" "test" "__tests__" "spec"
    "docs" "public" "static" "assets"
    "prisma" "migrations" "scripts" "config" "notebooks"
    "node_modules" ".next" ".git" ".claude" ".claude_plans" ".claude_prompts" ".claude_research"
    ".playwright-mcp" ".github" ".vscode" ".idea"
    "dist" "build" "out" ".cache"
    "vendor" "target" "pkg"
    "data" "fixtures" "mocks" "stubs"
    "status" "catalog" "templates"
)

is_allowed_root_file() {
    local filename="$1"
    for pattern in "${ALLOWED_ROOT_FILES[@]}"; do
        # shellcheck disable=SC2254
        case "$filename" in $pattern) return 0 ;; esac
    done
    return 1
}

is_allowed_root_dir() {
    local dirname="$1"
    for allowed in "${ALLOWED_ROOT_DIRS[@]}"; do
        [[ "$dirname" == "$allowed" ]] && return 0
    done
    return 1
}

clean_project() {
    local project_path="$1"

    if [[ ! -d "$project_path" ]]; then
        log_warn "Not a directory: $project_path"
        return 1
    fi

    log_info "Cleaning: $project_path"
    echo ""

    # 1. Create standard directories
    for dir in docs scripts notebooks; do
        if [[ ! -d "$project_path/$dir" ]]; then
            if $DRY_RUN; then
                log_dry "Create directory: $dir/"
            else
                mkdir -p "$project_path/$dir"
                log_action "Created: $dir/"
            fi
        fi
    done

    # 2. Move misplaced files from root
    local moved=0
    for file in "$project_path"/*; do
        [[ ! -f "$file" ]] && continue
        local filename
        filename=$(basename "$file")

        if is_allowed_root_file "$filename"; then
            continue
        fi

        # Determine destination based on extension
        local dest=""
        case "$filename" in
            *.md)  dest="docs" ;;
            *.py)  dest="scripts" ;;
            *.sh)  dest="scripts" ;;
            *.ipynb) dest="notebooks" ;;
            *.log) dest=".logs" ;;
            *.tmp|*.bak) dest="DELETE" ;;
        esac

        if [[ -n "$dest" ]]; then
            if [[ "$dest" == "DELETE" ]]; then
                if $DRY_RUN; then
                    log_dry "Delete: $filename"
                else
                    rm "$file"
                    log_action "Deleted: $filename"
                fi
            else
                if $DRY_RUN; then
                    log_dry "Move $filename -> $dest/"
                else
                    mkdir -p "$project_path/$dest"
                    mv "$file" "$project_path/$dest/"
                    log_action "Moved: $filename -> $dest/"
                fi
            fi
            ((moved++))
        fi
    done

    # 3. Clean .DS_Store files
    local ds_count
    ds_count=$(find "$project_path" -name ".DS_Store" 2>/dev/null | wc -l)
    if [[ "$ds_count" -gt 0 ]]; then
        if $DRY_RUN; then
            log_dry "Delete $ds_count .DS_Store files"
        else
            find "$project_path" -name ".DS_Store" -delete
            log_action "Deleted $ds_count .DS_Store files"
        fi
    fi

    # 4. Clean old temp files
    local tmp_count
    tmp_count=$(find "$project_path" \( -name "*.tmp" -o -name "*.bak" \) -mtime +7 2>/dev/null | wc -l)
    if [[ "$tmp_count" -gt 0 ]]; then
        if $DRY_RUN; then
            log_dry "Delete $tmp_count stale temp files (>7 days old)"
        else
            find "$project_path" \( -name "*.tmp" -o -name "*.bak" \) -mtime +7 -delete
            log_action "Deleted $tmp_count stale temp files"
        fi
    fi

    # 5. Clean old log files
    local log_count
    log_count=$(find "$project_path" -maxdepth 1 -name "*.log" -mtime +7 2>/dev/null | wc -l)
    if [[ "$log_count" -gt 0 ]]; then
        if $DRY_RUN; then
            log_dry "Delete $log_count stale log files from root (>7 days old)"
        else
            find "$project_path" -maxdepth 1 -name "*.log" -mtime +7 -delete
            log_action "Deleted $log_count stale log files from root"
        fi
    fi

    echo ""
    log_info "Done cleaning: $(basename "$project_path") ($moved files relocated)"
    echo ""
}

# Parse arguments
if [[ $# -eq 0 ]]; then
    echo "Usage: $0 [--dry-run] [--all | /path/to/project]"
    exit 1
fi

TARGET=""
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --all) TARGET="__all__" ;;
        *) TARGET="$arg" ;;
    esac
done

if [[ "$TARGET" == "__all__" ]]; then
    # Clean all managed projects from config
    if [[ -f "$CONFIG_PATH" ]]; then
        projects=$(python3 -c "
import json
with open('$CONFIG_PATH') as f:
    config = json.load(f)
for p in config.get('managed_projects', []):
    print(p['path'])
")
        while IFS= read -r project; do
            [[ -n "$project" ]] && clean_project "$project"
        done <<< "$projects"
    else
        log_warn "No config.json found. Run project-scanner.py --register first."
        exit 1
    fi
else
    clean_project "$TARGET"
fi
