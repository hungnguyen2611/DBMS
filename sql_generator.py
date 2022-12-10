import click
import errno
import os
import pandas as pd

def double_single_quote(sentence:str):
    sentence = sentence.replace("'", "''")
    return sentence

@click.command()
@click.option('--generate', '-g', help='Change TEXT to generate excel file into SQL insert')
@click.option('--outputdir', '-o', help='Change TEXT to create directory output file')




def main(generate, outputdir):
    try:
        # Validate generate file can not be None
        if generate is None:
            raise TypeError

        # Check if outputdir is not None
        if outputdir != None:
            try:
                # Create a directory
                os.makedirs(outputdir)
                outputdir = "{}/".format(outputdir)
            except OSError as exc:
                # If directory is exists use this directory
                if exc.errno == errno.EEXIST:
                    outputdir = "{}/".format(outputdir)
        file = pd.ExcelFile(generate)
        for sheet_name in file.sheet_names:
            data = file.parse(sheet_name)
            filename = "{}{}.sql".format(outputdir, sheet_name)
            click.echo("### {}:".format(filename))
            write_file = open(filename, "w")
            for i, _ in data.iterrows():
                field_names = ", ".join(list(data.columns))
                rows = list()
                for column in data.columns:
                    if column == 'about' or column == 'name' or column=='title':
                        rows.append(double_single_quote(str(data[column][i])))
                    elif column == 'author_id':
                        if data[column][i] != data[column][i]:
                            rows.append('nan')
                        else:
                            rows.append(str(int(data[column][i])))
                    else:
                        rows.append(str(data[column][i]))
                row_values = "'" + "', '".join(rows) + "'"
                click.echo("INSERT INTO {} ({}) VALUES ({});".format(sheet_name, field_names, row_values))
                write_file.write("INSERT INTO {} ({}) VALUES ({});\n".format(sheet_name, field_names, row_values))
            write_file.close()
    except TypeError as e:
        click.echo("Error: Unknown generate file! Type -h for help.")

if __name__ == "__main__":
    main()






