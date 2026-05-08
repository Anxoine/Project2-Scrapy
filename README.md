# Project 2 Submission

This repository contains fixes implemented for Scrapy issues as part of the course project.

## Branch
All current work is combined in the `final-submission` branch.

## Issues Fixed (Current Progress)

- #1615: FilesPipeline now correctly accepts valid 2xx HTTP responses instead of only 200
- #1163: FormRequest now raises a ValueError when formname or formid does not match any form
- #7010: scrapy settings --get does not account for add-ons
- #6047: Improved unhandled exception handling for Crawler*.crawl()
- #955: Fixed Windows file URI handling to ensure correct file output paths
- #2141: Redirect handling now correct resets download_slot when redirecting across domains
- #899: Exceptions raised in downloader middleware are quietly suppressed

## Notes
All fixes were implemented following Scrapy's code structure and existing test patterns.

For Issue #1163: https://github.com/scrapy/scrapy/pull/7438

For Issue #1615: https://github.com/scrapy/scrapy/pull/7411

Additional issues and fixes will be added to this branch as the project progresses.
