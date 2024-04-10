import os
import nbformat

# Author: Sparsh Trivedy
# Date: 2024-03-10
# script for UBC's CPSC 330.
# This script extracts answers from the solutions of the homeworks and saves them in a separate ipynb file.
# The script assumes that the solutions are in the same directory as the script and that the solutions are named as hwX_sol (Y).ipynb
# where X is the homework number and Y is the download number.
# I recommend downloading the sample solution as hwX_sol.ipynb so thet every successive download is named as hwX_sol (1).ipynb, hwX_sol (2).ipynb, etc.
# I recommend downloading sets of 25-50 solutions at a time to avoid any issues with the script.
# A note to TAs: Feel free to use and modify this script as you see fit. I hope it makes your life easier.

# some variables to set before running the script
final_answers = []
directory_path = '/Users/sparshtrivedy/Downloads'
cell_name = 'Solution_2_5'
file_prefix = 'hw7_sol'
output_file_name = 'answers.ipynb'

def extract_answer_cell_for_specified_question(notebook_path, question, file):
    with open(notebook_path, 'r') as f:
        nb = nbformat.read(f, as_version=4)
    
    cells = []
    for cell in nb.cells:
        # we are assuming that the question is in a markdown cell - a safe assumption for our homeworks
        if cell.cell_type == 'markdown':
            # if the question is found in the cell, add the cell to the answers list
            if question in cell.source:
                # first append the cell that contains the file name so it is easy to track the source of the answer
                cell.source = cell.source.replace(cell_name, file)
                cells.append(cell)
                # move to the next cell and keep adding to the answer until we reach the next question
                cell_index = nb.cells.index(cell) + 1
                while cell_index < len(nb.cells) and 'BEGIN QUESTION' not in nb.cells[cell_index].source:
                    cells.append(nb.cells[cell_index])
                    cell_index += 1
                break
    return cells

def save_extracted_answers_into_output_file(extracted_answers, output_file):
    # save the answers in a separate ipynb file
    with open(output_file, 'w') as f:
        nb = nbformat.v4.new_notebook()
        for answer in extracted_answers:
            # if the cell is a code cell, add it as a code cell in the new notebook
            if answer.cell_type == 'code':
                nb.cells.append(nbformat.v4.new_code_cell(source=answer.source))
                # if the cell has outputs, add them to the new notebook as well
                if answer.outputs:
                    for output in answer.outputs:
                        nb.cells[-1].outputs.append(output)
            else:
                # if the cell is a markdown cell, add it as a markdown cell in the new notebook
                nb.cells.append(nbformat.v4.new_markdown_cell(source=answer.source))
        nbformat.write(nb, f)
    return extracted_answers

for root, dirs, files in os.walk(directory_path):
    for file in files:
        file = file.split('-')[0]
        if file.startswith(file_prefix) and file.endswith('.ipynb'):
            ans = extract_answer_cell_for_specified_question(directory_path + '/' + file, cell_name, file)
            if ans:
                final_answers += ans
            else:
                print('No answers found for', file)

save_extracted_answers_into_output_file(final_answers, output_file_name)
