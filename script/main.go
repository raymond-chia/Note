package main

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

func main() {
	fmt.Println(os.Args)
	switch os.Args[1] {
	case "git-fetch":
		err := GitFetch()
		if err != nil {
			panic(err)
		}
	}
}

func GitFetch() error {
	// 獲取當前目錄
	currentDir, err := os.Getwd()
	if err != nil {
		return fmt.Errorf("Error getting current directory: %w", err)
	}

	// 遍歷所有子目錄
	err = filepath.Walk(currentDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		// 如果是目錄且包含 .git 文件夾
		if info.IsDir() && isGitRepo(path) {
			fmt.Printf("Processing repository: %s\n", path)

			// 執行 git fetch origin --prune
			_, err := runGitCommand(path, "fetch", "origin", "--prune")
			if err != nil {
				return fmt.Errorf("Error fetching in %s: %w\n", path, err)
			}

			// 獲取默認分支
			defaultBranch, err := getDefaultBranch(path)
			if err != nil {
				return fmt.Errorf("Error getting default branch for %s: %w\n", path, err)
			}

			fmt.Printf("Checking out to branch: %q\n", defaultBranch)

			// 切換到默認分支
			_, err = runGitCommand(path, "checkout", "origin/"+defaultBranch)
			if err != nil {
				return fmt.Errorf("Error switching to default branch in %s: %w\n", path, err)
			}

			// 刪除 local 默認分支
			_, err = runGitCommand(path, "branch", "-d", defaultBranch)
			if err != nil && !strings.Contains(err.Error(), "not found") {
				return fmt.Errorf("Error deleting local default branch in %s: %w\n", path, err)
			}
			// 印所有分支, 不在乎是否成功
			output, _ := runGitCommand(path, "branch")
			fmt.Println("Remaining branches:\n", output)

			fmt.Printf("Successfully updated %s to %s\n", path, defaultBranch)
		}

		return nil
	})

	if err != nil {
		return fmt.Errorf("Error walking through directories: %w\n", err)
	}
	return nil
}

func isGitRepo(path string) bool {
	_, err := os.Stat(filepath.Join(path, ".git"))
	return err == nil
}

func runGitCommand(dir string, args ...string) (string, error) {
	cmd := exec.Command("git", args...)
	cmd.Dir = dir
	output, err := cmd.CombinedOutput()
	if err != nil {
		return "", fmt.Errorf("%v: %s", err, string(output))
	}
	return string(output), nil
}

func getDefaultBranch(dir string) (string, error) {
	cmd := exec.Command("git", "remote", "show", "origin")
	cmd.Dir = dir
	output, err := cmd.Output()
	if err != nil {
		return "", err
	}

	// 解析輸出以獲取默認分支名稱
	lines := string(output)
	for _, line := range strings.Split(lines, "\n") {
		if strings.Contains(line, "HEAD branch:") {
			return strings.TrimSpace(strings.TrimPrefix(strings.TrimSpace(line), "HEAD branch:")), nil
		}
	}

	return "", fmt.Errorf("unable to determine default branch")
}
